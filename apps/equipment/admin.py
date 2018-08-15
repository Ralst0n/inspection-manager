from django.contrib import admin
from .models import Equipment, Checkout
# Register your models here.
class CheckoutInline(admin.TabularInline):
    model = Checkout

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        filter which projects show in list view
        """
        groups = []
        for group in request.user.groups.all():
            groups.append(str(group))
        if request.user.is_superuser:
            return Equipment.objects.all()
        else:
            return Equipment.objects.all().filter(office__in=groups)
    list_display = ('name', 'device', 'serial_number')
    inlines = [CheckoutInline]
@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    pass
