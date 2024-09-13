from django.contrib import admin

# Register your models here.
from PickDropApp.models import * 

class user_registration_admin(admin.ModelAdmin):
    try:
        list_display = ('username', 'email', 'password','mobile')
    except Exception as e:
        print(e)
admin.site.register(user_registration_model, user_registration_admin)

class professional_registration_admin(admin.ModelAdmin):
    try:
        list_display = ('name', 'email', 'password','mobile','specialization','drone_type','load_capacity','location')
    except Exception as e:
        print(e)
admin.site.register(professional_registration_model,professional_registration_admin)

class user_drashboard_admin(admin.ModelAdmin):
    try:
        list_display = ('pickup','dropoff','weight')
    except Exception as e:
        print(e)

admin.site.register(user_dashboard_model,user_drashboard_admin)

