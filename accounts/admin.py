from django.contrib import admin
from .models import UserAccounts,Blogs,City

# Register your models here.
admin.site.register(UserAccounts)
admin.site.register(Blogs)
admin.site.register(City)