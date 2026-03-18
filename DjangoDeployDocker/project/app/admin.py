from django.contrib import admin
from .models import User, Message, Chat, Profile

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Profile)
# Register your models here.
