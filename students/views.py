from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Course, StudyMaterial, Question, TestResult
import json
import random
import os
import io
from datetime import datetime


# ─── HOME ────────────────────────────────────────────────────────────────────
def home(request):
    courses = Course.objects.all()
    total_students = TestResult.objects.values('student_email').distinct().count()
    total_tests = TestResult.objects.count()
    pass_rate = TestResult.objects.filter(passed=True).count()
    return render(request, 'home.html', {
        'courses': courses,
        'total_students': total_students,
        'total_tests': total_tests,
        'pass_rate': pass_rate,
    })


# ─── COURSES ─────────────────────────────────────────────────────────────────
def courses(request):
    courses = Course.objects.annotate(
        material_count=Count('materials', distinct=True),
        question_count=Count('questions', distinct=True)
    )
    return render(request, 'courses.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all()
    question_count = course.questions.count()
    results = course.results.order_by('-taken_at')[:5]
    return render(request, 'course_detail.html', {
        'course': course,
        'materials': materials,
        'question_count': question_count,
        'recent_results': results,
    })


# ─── PDF DOWNLOAD ─────────────────────────────────────────────────────────────
def download_pdf(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    if not material.pdf_file:
        raise Http404("PDF not found")
    response = FileResponse(
        material.pdf_file.open('rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'attachment; filename="{material.title}.pdf"'
    return response


def view_pdf(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    if not material.pdf_file:
        raise Http404("PDF not found")
    response = FileResponse(
        material.pdf_file.open('rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'inline; filename="{material.title}.pdf"'
    return response


# ─── TEST / APTITUDE ──────────────────────────────────────────────────────────
def start_test(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    all_questions = list(course.questions.all())

    if len(all_questions) < 5:
        messages.error(request, "Not enough questions available for this test. Please contact admin.")
        return redirect('course_detail', course_id=course_id)

    # Pick 20 random questions (or all if fewer than 20)
    count = min(20, len(all_questions))
    selected = random.sample(all_questions, count)

    # Shuffle options for each question
    test_questions = []
    for q in selected:
        options = [
            ('A', q.option_a),
            ('B', q.option_b),
            ('C', q.option_c),
            ('D', q.option_d),
        ]
        random.shuffle(options)
        # Build mapping: new_key -> original_key
        answer_map = {}
        new_options = {}
        for new_key, (orig_key, text) in zip(['A', 'B', 'C', 'D'], options):
            new_options[new_key] = text
            answer_map[new_key] = orig_key  # maps new position to original option

        # What is the new key for the correct answer?
        correct_new = None
        for nk, ok in answer_map.items():
            if ok == q.correct_answer:
                correct_new = nk
                break

        test_questions.append({
            'id': q.id,
            'text': q.question_text,
            'options': new_options,
            'answer_map': answer_map,
            'correct_shuffled': correct_new,
        })

    # Store in session
    request.session['test_course_id'] = course_id
    request.session['test_questions'] = [
        {
            'id': tq['id'],
            'text': tq['text'],
            'options': tq['options'],
            'correct_shuffled': tq['correct_shuffled'],
            'answer_map': tq['answer_map'],
        }
        for tq in test_questions
    ]

    return render(request, 'test.html', {
        'course': course,
        'questions': test_questions,
        'total': count,
    })


def submit_test(request, course_id):
    if request.method != 'POST':
        return redirect('start_test', course_id=course_id)

    course = get_object_or_404(Course, id=course_id)
    session_questions = request.session.get('test_questions', [])

    if not session_questions:
        messages.error(request, "Session expired. Please start the test again.")
        return redirect('start_test', course_id=course_id)

    student_name = request.POST.get('student_name', '').strip()
    student_email = request.POST.get('student_email', '').strip()

    if not student_name:
        messages.error(request, "Please enter your name.")
        return redirect('start_test', course_id=course_id)

    score = 0
    total = len(session_questions)
    result_details = []

    for sq in session_questions:
        qid = str(sq['id'])
        chosen = request.POST.get(f'q_{qid}', '')
        correct_shuffled = sq['correct_shuffled']
        is_correct = (chosen == correct_shuffled)
        if is_correct:
            score += 1

        result_details.append({
            'id': sq['id'],
            'text': sq['text'],
            'options': sq['options'],
            'chosen': chosen,
            'correct': correct_shuffled,
            'is_correct': is_correct,
            'explanation': '',
        })

    percentage = (score / total) * 100
    passed = percentage >= 60

    # Fetch explanations
    question_ids = [sq['id'] for sq in session_questions]
    questions_db = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    for rd in result_details:
        q_obj = questions_db.get(rd['id'])
        if q_obj:
            rd['explanation'] = q_obj.explanation

    answers_json = json.dumps({str(rd['id']): rd['chosen'] for rd in result_details})
    questions_json = json.dumps(question_ids)

    test_result = TestResult.objects.create(
        student_name=student_name,
        student_email=student_email,
        course=course,
        score=score,
        total_questions=total,
        percentage=percentage,
        answers_json=answers_json,
        questions_json=questions_json,
        passed=passed,
        certificate_issued=passed,
    )

    # Clear session
    if 'test_questions' in request.session:
        del request.session['test_questions']
    if 'test_course_id' in request.session:
        del request.session['test_course_id']

    return render(request, 'test_result.html', {
        'course': course,
        'score': score,
        'total': total,
        'percentage': percentage,
        'passed': passed,
        'student_name': student_name,
        'result_details': result_details,
        'test_result': test_result,
    })


# ─── CERTIFICATE ──────────────────────────────────────────────────────────────
def download_certificate(request, result_id):
    result = get_object_or_404(TestResult, id=result_id)
    if not result.passed:
        raise Http404("Certificate not available - test not passed")

    try:
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import HexColor
    except ImportError:
        return HttpResponse("ReportLab not installed. Run: pip install reportlab", status=500)

    buffer = io.BytesIO()
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Background gradient effect
    c.setFillColor(HexColor('#0f172a'))
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    # Gold decorative border
    border_colors = ['#f59e0b', '#fbbf24', '#f59e0b']
    for i, bc in enumerate(border_colors):
        margin = 15 + i * 8
        c.setStrokeColor(HexColor(bc))
        c.setLineWidth(2 if i == 1 else 1)
        c.roundRect(margin, margin, page_width - 2*margin, page_height - 2*margin, 10, fill=0, stroke=1)

    # Inner card
    card_x, card_y = 60, 60
    card_w, card_h = page_width - 120, page_height - 120
    c.setFillColor(HexColor('#1e293b'))
    c.roundRect(card_x, card_y, card_w, card_h, 8, fill=1, stroke=0)

    # Top decorative bar
    c.setFillColor(HexColor('#f59e0b'))
    c.rect(card_x, card_y + card_h - 12, card_w, 12, fill=1, stroke=0)

    # Bottom decorative bar
    c.setFillColor(HexColor('#f59e0b'))
    c.rect(card_x, card_y, card_w, 8, fill=1, stroke=0)

    # Stars decoration
    star_y = page_height / 2 + 60
    for sx in [120, 145, 170, page_width - 120, page_width - 145, page_width - 170]:
        c.setFillColor(HexColor('#f59e0b'))
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(sx, star_y, '★')

    # EduPortal header
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#f59e0b'))
    c.drawCentredString(page_width / 2, page_height - 105, '🎓  E D U P O R T A L  PRO')

    # Certificate of Achievement
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(page_width / 2, page_height - 130, '─────────────────────────────────────────────')

    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(HexColor('#f8fafc'))
    c.drawCentredString(page_width / 2, page_height - 175, 'Certificate of Achievement')

    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(page_width / 2, page_height - 200, 'This is to proudly certify that')

    # Student name
    c.setFont("Helvetica-BoldOblique", 38)
    c.setFillColor(HexColor('#f59e0b'))
    c.drawCentredString(page_width / 2, page_height - 250, result.student_name)

    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(page_width / 2, page_height - 275, 'has successfully completed the aptitude test in')

    # Course name
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(HexColor('#60a5fa'))
    c.drawCentredString(page_width / 2, page_height - 310, result.course.title)

    # Score box
    box_x = page_width / 2 - 80
    c.setFillColor(HexColor('#0f172a'))
    c.roundRect(box_x, page_height - 365, 160, 45, 6, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#f59e0b'))
    c.setLineWidth(1.5)
    c.roundRect(box_x, page_height - 365, 160, 45, 6, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#f59e0b'))
    c.drawCentredString(page_width / 2, page_height - 345, f'Score: {result.score}/{result.total_questions}  ({result.percentage:.1f}%)')

    # Date and certificate ID
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor('#64748b'))
    date_str = result.taken_at.strftime('%B %d, %Y')
    c.drawCentredString(page_width / 2, page_height - 390, f'Date of Issue: {date_str}   |   Certificate ID: EP-{result.id:05d}')

    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor('#475569'))
    c.drawCentredString(page_width / 2, 85, 'This certificate is issued by EduPortal Pro and confirms successful completion of the aptitude assessment.')

    c.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    safe_name = result.student_name.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="Certificate_{safe_name}_{result.course.subject}.pdf"'
    return response


# ─── CONTACT ─────────────────────────────────────────────────────────────────
def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thank you! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')


# ─── LEADERBOARD ─────────────────────────────────────────────────────────────
def leaderboard(request):
    results = TestResult.objects.filter(passed=True).order_by('-percentage', '-score')[:50]
    courses = Course.objects.all()
    return render(request, 'leaderboard.html', {'results': results, 'courses': courses})
