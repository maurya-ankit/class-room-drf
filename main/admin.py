from django.contrib import admin

# Register your models here.

from .models import Classroom,Membership,ClassroomPost,ClassroomPostComment

# admin.site.register(User)

admin.site.register(Classroom)

admin.site.register(Membership)

admin.site.register(ClassroomPost)

admin.site.register(ClassroomPostComment)
