from django.contrib import admin

from .models import Room, Question, Contestant, Tag

class ContestantInline(admin.TabularInline):
    model = Contestant
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    exclude = ['code']
    inlines = [
        ContestantInline,
    ]

class QuestionAdmin(admin.ModelAdmin):
    pass

class ContestantAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Tag, TagAdmin)