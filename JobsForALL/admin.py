from django.contrib import admin

# Register your models here.


from .models import User,Employer,Employee


admin.site.register(User)

admin.site.register(Employer)

admin.site.register(Employee)