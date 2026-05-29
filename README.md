# 🎓 EduPortal Pro

A full-featured education portal built with Django.

## Features
- 📚 Multiple courses with study materials
- 📄 PDF download & in-browser reading
- 🧠 20-question aptitude tests (randomized every attempt)
- 🏆 PDF certificates on passing (60%+)
- ✅ Full answer review with explanations after submission
- 📊 Leaderboard of top performers
- 📱 Responsive design

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Seed Sample Data (4 courses + 25 questions each)
```bash
python seed_data.py
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

### Admin Panel
Go to http://127.0.0.1:8000/admin to:
- Add/edit courses
- Upload PDF study materials
- Add questions to courses
- View test results

## Uploading PDF Materials
1. Login to admin panel
2. Click "Courses" → select a course
3. Scroll to "Study Materials" section
4. Add a PDF file

## Test System
- Each test picks 20 random questions from the question bank
- Options are shuffled each time
- 30-minute timer
- Pass mark: 60% (12/20)
- After submission: full answer review with explanations
- Pass → Download PDF certificate instantly

## Adding More Questions
Use the admin panel → Questions → Add Question
Select the course and fill in the 4 options + correct answer + explanation.
