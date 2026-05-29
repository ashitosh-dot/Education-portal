from django.contrib import admin
from .models import Course, StudyMaterial, Question, TestResult


class StudyMaterialInline(admin.TabularInline):
    model = StudyMaterial
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'level', 'duration']
    inlines = [StudyMaterialInline, QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'course', 'correct_answer']
    list_filter = ['course']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'course', 'score', 'percentage', 'passed', 'taken_at']
    list_filter = ['course', 'passed']
    readonly_fields = ['taken_at']


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'uploaded_at']
