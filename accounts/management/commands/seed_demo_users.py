"""
Create demo accounts matching the LIS testing checklist.

Password for all: Pass@1234
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import UserProfile

# Same as README / manual shell checklist
DEMO_USERS = [
    ('physician1', 'Dr. Ravi Kumar', 'Physician', 'EMP001', 'Senior Physician', 'Pathology'),
    ('nurse1', 'Nurse Priya', 'Nurse', 'EMP002', 'Staff Nurse', 'Ward'),
    ('phlebotomist1', 'Sam Collector', 'Phlebotomist', 'EMP003', 'Phlebotomist', 'Lab'),
    ('techlab1', 'Tech Arun', 'LabTechnician', 'EMP004', 'Lab Technician', 'Pathology'),
]
PASSWORD = 'Pass@1234'


class Command(BaseCommand):
    help = 'Create or update the four role-based demo users (checklist Step 1).'

    def handle(self, *args, **options):
        for username, full_name, role, emp_id, designation, dept in DEMO_USERS:
            user, created = User.objects.get_or_create(username=username, defaults={'email': ''})
            user.set_password(PASSWORD)
            user.save()

            profile, pc = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': emp_id,
                    'full_name': full_name,
                    'role': role,
                    'designation': designation,
                    'department': dept,
                    'status': 'Active',
                },
            )
            if not pc:
                profile.employee_id = emp_id
                profile.full_name = full_name
                profile.role = role
                profile.designation = designation
                profile.department = dept
                profile.status = 'Active'
                profile.save()

            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} {username} ({role})"))

        self.stdout.write('')
        self.stdout.write(self.style.WARNING(f'Password for all demo users: {PASSWORD}'))
        self.stdout.write('Usernames: physician1, nurse1, phlebotomist1, techlab1')
