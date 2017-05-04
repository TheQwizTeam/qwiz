from django.contrib import admin

from .models import Room, Question, Contestant, QuestionVault

class ContestantInline(admin.TabularInline):
    model = Contestant
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionVaultInline(admin.TabularInline):
    model = QuestionVault
    exttra = 1

class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    inlines = [QuestionInline]
    inlines = [ContestantInline]

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'field': ['room']}),
        inlines = [QuestionVaultInline]
    ]

admin.site.register(Room, RoomAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Contestant)
admin.site.register(QuestionVault)