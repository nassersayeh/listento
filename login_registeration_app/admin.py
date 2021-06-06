from django.contrib import admin
from login_registeration_app.models import User,Gender,Role
from music_app.models import Music

admin.site.register(User)
admin.site.register(Music)
admin.site.register(Gender)
admin.site.register(Role)

# Register your models here.
