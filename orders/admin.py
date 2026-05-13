from django.contrib import admin
from .models import OrderTransaction, OrderLine

admin.site.register(OrderTransaction)
admin.site.register(OrderLine)
