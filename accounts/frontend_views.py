"""
Django template-based frontend views.
"""
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET

from patients.models import PatientMaster
from orders.models import OrderTransaction, OrderLine
from labtests.models import TestMenuMaster, AssayMaster
from accounts.models import UserProfile, UserAccessMaster
from accounts.utils import ensure_user_profile
from accounts.frontend_decorators import role_required
from results.models import Result


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            profile = ensure_user_profile(user)
            if profile.status != 'Active':
                messages.error(request, 'Account is inactive or locked.')
                return render(request, 'login.html')
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    profile = request.user.profile
    role = profile.role
    context = {
        'role': role,
        'profile': profile,
        'total_patients': PatientMaster.objects.count(),
        'pending_orders': OrderTransaction.objects.filter(order_status=1).count(),
        'collected_orders': OrderTransaction.objects.filter(order_status=2).count(),
        'inlab_orders': OrderTransaction.objects.filter(order_status=3).count(),
        'completed_today': OrderTransaction.objects.filter(order_status=4).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
@role_required('Physician', 'Nurse')
def patient_list(request):
    search = request.GET.get('search', '')
    patients = PatientMaster.objects.all()
    if search:
        patients = patients.filter(patient_name__icontains=search) | patients.filter(mrn__icontains=search)
    return render(request, 'patient_list.html', {'patients': patients, 'search': search})


@login_required
@role_required('Physician', 'Nurse')
def patient_register(request):
    if request.method == 'POST':
        mrn = request.POST.get('mrn') or PatientMaster.generate_mrn()
        try:
            PatientMaster.objects.create(
                mrn=mrn,
                patient_name=request.POST['patient_name'],
                age=request.POST['age'],
                gender=request.POST['gender'],
                nationality=request.POST['nationality'],
                dob=request.POST.get('dob') or None,
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                status=request.POST.get('status', 'Active'),
            )
            messages.success(request, f'Patient registered successfully with MRN: {mrn}')
            return redirect('patient_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    auto_mrn = PatientMaster.generate_mrn()
    return render(request, 'patient_register.html', {'auto_mrn': auto_mrn})


@login_required
@role_required('Physician', 'Nurse')
def patient_edit(request, pk):
    patient = PatientMaster.objects.get(pk=pk)
    if request.method == 'POST':
        patient.patient_name = request.POST['patient_name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.nationality = request.POST['nationality']
        patient.dob = request.POST.get('dob') or None
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email')
        patient.status = request.POST.get('status', 'Active')
        patient.save()
        messages.success(request, 'Patient updated successfully.')
        return redirect('patient_list')
    return render(request, 'patient_register.html', {'patient': patient, 'edit': True})


@login_required
@role_required('Physician', 'Nurse')
def order_entry(request):
    patients = PatientMaster.objects.filter(status='Active')
    menus = TestMenuMaster.objects.filter(status='Active').prefetch_related('assays')
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        assay_ids = request.POST.getlist('assay_ids')
        notes = request.POST.get('notes', '')
        if not assay_ids:
            messages.error(request, 'Please add at least one test to the order.')
        else:
            profile = request.user.profile
            order = OrderTransaction.objects.create(
                order_no=OrderTransaction.generate_order_no(),
                patient_id=patient_id,
                ordered_by=profile,
                notes=notes,
            )
            for aid in assay_ids:
                OrderLine.objects.create(order=order, assay_id=aid)
            messages.success(request, f'Order {order.order_no} placed successfully.')
            return redirect('order_list')
    return render(request, 'order_entry.html', {'patients': patients, 'menus': menus})


@login_required
@role_required('Physician', 'Nurse')
def order_list(request):
    orders = OrderTransaction.objects.select_related('patient').prefetch_related('lines')
    return render(request, 'order_list.html', {'orders': orders})


@login_required
@role_required('Phlebotomist')
def phlebotomist_worklist(request):
    status_filter = request.GET.get('status', '1')
    orders = OrderTransaction.objects.select_related('patient').prefetch_related('lines')
    if status_filter and status_filter != 'all':
        orders = orders.filter(order_status=int(status_filter))
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = OrderTransaction.objects.get(pk=order_id)
        if order.order_status == 1:
            from django.utils import timezone
            order.order_status = 2
            order.collected_by = request.user.profile
            order.collected_at = timezone.now()
            order.save()
            messages.success(request, f'Sample collected for order {order.order_no}.')
        return redirect('phlebotomist_worklist')
    return render(request, 'phlebotomist_worklist.html', {'orders': orders, 'status_filter': status_filter})


@login_required
@role_required('LabTechnician')
def technician_worklist(request):
    status_filter = request.GET.get('status', '2')
    orders = OrderTransaction.objects.select_related('patient').prefetch_related('lines__assay', 'results')
    if status_filter and status_filter != 'all':
        orders = orders.filter(order_status=int(status_filter))
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        order = OrderTransaction.objects.get(pk=order_id)
        profile = request.user.profile
        if action == 'mark_inlab' and order.order_status == 2:
            from django.utils import timezone
            order.order_status = 3
            order.received_by = profile
            order.received_at = timezone.now()
            order.save()
            messages.success(request, f'Order {order.order_no} moved to In-Lab.')
        elif action == 'save_results' and order.order_status in (3, 4):
            for line in order.lines.all():
                val = request.POST.get(f'result_{line.assay.id}')
                if val:
                    Result.objects.update_or_create(
                        order=order, assay=line.assay,
                        defaults={
                            'result_value': val,
                            'unit': request.POST.get(f'unit_{line.assay.id}', line.assay.unit or ''),
                            'normal_range': request.POST.get(f'normal_{line.assay.id}', line.assay.normal_range or ''),
                            'flag': request.POST.get(f'flag_{line.assay.id}', ''),
                            'remarks': request.POST.get(f'remarks_{line.assay.id}', ''),
                            'entered_by': profile,
                        }
                    )
            order.order_status = 4
            order.save()
            messages.success(request, f'Results saved. Order {order.order_no} is Completed.')
        return redirect('technician_worklist')
    return render(request, 'technician_worklist.html', {'orders': orders, 'status_filter': status_filter})


@login_required
@role_required('Physician', 'Nurse')
def lab_report(request, pk):
    order = OrderTransaction.objects.select_related(
        'patient', 'ordered_by', 'collected_by', 'received_by'
    ).prefetch_related('results__assay').get(pk=pk)
    if order.order_status != 4:
        messages.error(request, 'Report is not available. The order must be Completed.')
        return redirect('order_list')
    return render(request, 'lab_report.html', {'order': order})


@login_required
@role_required('Admin')
def test_management(request):
    menus = TestMenuMaster.objects.prefetch_related('assays').all()
    return render(request, 'test_management.html', {'menus': menus})


@login_required
@role_required('Admin')
def user_management(request):
    users = UserProfile.objects.select_related('user').all()
    access_rules = UserAccessMaster.objects.all()
    return render(request, 'user_management.html', {'users': users, 'access_rules': access_rules})


@login_required
@role_required('Physician', 'Nurse')
@require_GET
def generate_mrn_ajax(request):
    return JsonResponse({'mrn': PatientMaster.generate_mrn()})
