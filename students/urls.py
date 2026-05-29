from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/test/', views.start_test, name='start_test'),
    path('courses/<int:course_id>/test/submit/', views.submit_test, name='submit_test'),
    path('certificate/<int:result_id>/', views.download_certificate, name='download_certificate'),
    path('pdf/download/<int:material_id>/', views.download_pdf, name='download_pdf'),
    path('pdf/view/<int:material_id>/', views.view_pdf, name='view_pdf'),
    path('contact/', views.contact, name='contact'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
