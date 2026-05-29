from django.db import models
import json


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    duration = models.CharField(max_length=50, default="4 weeks")
    level = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ], default='Beginner')
    icon = models.CharField(max_length=10, default='📚')
    color = models.CharField(max_length=30, default='#4f46e5')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ])
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.title}: {self.question_text[:60]}"


class TestResult(models.Model):
    student_name = models.CharField(max_length=200)
    student_email = models.CharField(max_length=200, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    total_questions = models.IntegerField(default=20)
    percentage = models.FloatField()
    answers_json = models.TextField(default='{}')  # stores {question_id: chosen_answer}
    questions_json = models.TextField(default='[]')  # stores list of question ids used
    passed = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)
    taken_at = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        return json.loads(self.answers_json)

    def get_questions(self):
        return json.loads(self.questions_json)

    def __str__(self):
        return f"{self.student_name} - {self.course.title} - {self.percentage:.1f}%"
