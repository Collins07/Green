from django.contrib import admin
from farmers.models import Image, Profile,Follow

# Register your models here.
admin.site.register(Profile)
admin.site.register(Image)

admin.site.register(Follow)