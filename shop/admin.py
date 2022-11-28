from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session

admin.site.unregister(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','email']
    class Meta:
        model = User

admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Feedback)
admin.site.register(Session)
admin.site.register(ShippingAddress)






