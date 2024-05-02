from django.contrib import admin
from .models import Lesson, Comments, Photo

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Comments)
admin.site.register(Photo)
