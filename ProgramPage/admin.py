
from django.contrib import admin
from .models import Program, Semester, Subject, Note

class SemesterInline(admin.TabularInline):
    model = Semester
    extra = 2   # number of empty rows shown


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SemesterInline]

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'name')
    list_filter = ('program',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'semester')
    list_filter = ('semester__program', 'semester')
    search_fields = ('name',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'semester', 'subject', 'uploaded_by', 'uploaded_at')
    list_filter = ('semester__program', 'semester', 'subject')
    search_fields = ('title',)

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)
