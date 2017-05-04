from django.contrib import admin

from .models import Room, Question, Contestant

admin.site.register(Room)
admin.site.register(Question)
admin.site.register(Contestant)
