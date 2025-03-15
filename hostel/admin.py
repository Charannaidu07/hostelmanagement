from django.contrib import admin,messages
from .models import Feature, HostelStay, PaymentHistory,Announcement,ChatMessage,Outing
from datetime import date
from django.shortcuts import redirect
from django.urls import path
from django.utils.safestring import mark_safe
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_paid', 'payment_date', 'verified')
    list_filter = ('verified',)
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        for payment in queryset:
            payment.verified = True  
            payment.save()
    mark_as_verified.short_description = "Mark selected payments as Verified"
@admin.action(description="Approve and assign room")
def approve_hostel_stay(modeladmin, request, queryset):
    for stay in queryset:
        stay.status = "approved"
        stay.room_number = f"R{stay.id}" 
        stay.check_in = date.today()
        stay.save()

class HostelStayAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "check_in", "status", "room_number")
    list_filter = ("status", "gender")
    search_fields = ("user__username", "room_number")
# Register models
admin.site.register(Feature)
admin.site.register(HostelStay)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(Announcement)
admin.site.register(ChatMessage)
admin.site.register(Outing)