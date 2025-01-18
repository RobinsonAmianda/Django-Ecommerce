from django.contrib import admin

from user_auth.models import User , Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)

