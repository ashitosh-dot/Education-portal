"""
Run this script to populate sample courses and questions:
  python manage.py shell < seed_data.py
  OR
  python seed_data.py (from project root, with DJANGO_SETTINGS_MODULE set)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduPortal.settings')
django.setup()

from students.models import Course, Question

courses_data = [
    {
        'title': 'Python Programming',
        'subject': 'Python',
        'description': 'Master Python programming from basics to advanced concepts including OOP, file handling, and web development.',
        'level': 'Beginner',
        'duration': '6 weeks',
        'icon': '🐍',
        'color': '#3b82f6',
        'questions': [
            ("What is the output of print(type([]))?", "<class 'list'>", "<class 'array'>", "<class 'tuple'>", "None", "A", "A list's type is <class 'list'> in Python."),
            ("Which keyword is used to define a function in Python?", "fun", "def", "function", "define", "B", "The 'def' keyword is used to define functions in Python."),
            ("What does len('Hello') return?", "4", "5", "6", "Error", "B", "len() counts characters, 'Hello' has 5 characters."),
            ("Which of these is a valid Python comment?", "// comment", "/* comment */", "# comment", "<!-- comment -->", "C", "Python uses # for single-line comments."),
            ("What is the result of 10 % 3?", "3", "1", "0", "3.33", "B", "Modulo (%) returns the remainder. 10 % 3 = 1."),
            ("How do you create an empty dictionary?", "dict = []", "dict = {}", "dict = ()", "dict = set()", "B", "Empty dictionaries are created with {} or dict()."),
            ("Which method adds an element to a list?", "add()", "insert()", "append()", "push()", "C", "append() adds an element to the end of a list."),
            ("What is the correct way to open a file in Python?", "open('file.txt')", "file.open('file.txt')", "File('file.txt')", "read('file.txt')", "A", "The built-in open() function is used to open files."),
            ("What does 'self' refer to in a Python class?", "The class itself", "The instance of the class", "The parent class", "None", "B", "self refers to the current instance of the class."),
            ("Which Python data type is immutable?", "List", "Dictionary", "Set", "Tuple", "D", "Tuples are immutable — they cannot be changed after creation."),
            ("What is the output of bool(0)?", "True", "False", "0", "Error", "B", "0 is falsy in Python, so bool(0) returns False."),
            ("Which statement is used to handle exceptions in Python?", "catch", "try-except", "handle", "error", "B", "Python uses try-except blocks for exception handling."),
            ("What does __init__ method do?", "Initializes a module", "Is the constructor of a class", "Closes an object", "Returns a value", "B", "__init__ is called automatically when an object is created."),
            ("How do you import a module named 'math'?", "include math", "require math", "import math", "using math", "C", "Python uses the import statement to include modules."),
            ("What is list comprehension?", "A type of loop", "A concise way to create lists", "A method of list", "A sorting algorithm", "B", "List comprehension provides a shorter syntax to create lists."),
            ("Which operator is used for floor division?", "/", "//", "%", "**", "B", "// performs floor division, rounding down to nearest integer."),
            ("What does range(5) produce?", "1,2,3,4,5", "0,1,2,3,4", "0,1,2,3,4,5", "1,2,3,4", "B", "range(5) generates numbers 0 through 4 (5 exclusive)."),
            ("How do you convert string '42' to integer?", "str(42)", "int('42')", "integer('42')", "float('42')", "B", "int() converts a string to an integer."),
            ("What is a lambda function?", "A named function", "An anonymous function", "A class method", "A built-in function", "B", "Lambda functions are anonymous, one-line functions."),
            ("Which library is commonly used for data manipulation?", "NumPy", "Pandas", "Matplotlib", "Requests", "B", "Pandas is the go-to library for data manipulation and analysis."),
            ("What does 'pass' do in Python?", "Terminates function", "Does nothing", "Returns None", "Skips loop", "B", "pass is a null statement used as a placeholder."),
            ("How do you get all keys from a dictionary d?", "d.keys()", "d.values()", "keys(d)", "d.items()", "A", "dict.keys() returns all keys of a dictionary."),
            ("What is the purpose of 'else' in a for loop?", "Runs if loop breaks", "Runs after loop completes normally", "Always runs", "Is invalid", "B", "The else clause in a loop runs if the loop completes without break."),
            ("Which method removes and returns the last item of a list?", "remove()", "delete()", "pop()", "discard()", "C", "list.pop() removes and returns the last element by default."),
            ("What does zip() do?", "Compresses files", "Combines iterables element-wise", "Sorts lists", "Merges strings", "B", "zip() combines multiple iterables into tuples."),
        ]
    },
    {
        'title': 'Web Development Fundamentals',
        'subject': 'Web Development',
        'description': 'Learn HTML, CSS, and JavaScript to build modern, responsive websites from the ground up.',
        'level': 'Beginner',
        'duration': '8 weeks',
        'icon': '🌐',
        'color': '#f59e0b',
        'questions': [
            ("What does HTML stand for?", "Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language", "A", "HTML = HyperText Markup Language, the standard for web pages."),
            ("Which HTML tag is used for the largest heading?", "<h6>", "<heading>", "<h1>", "<head>", "C", "<h1> is the largest and most important heading tag."),
            ("What does CSS stand for?", "Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets", "B", "CSS = Cascading Style Sheets, used for styling web pages."),
            ("Which CSS property changes text color?", "font-color", "text-color", "color", "foreground", "C", "The color property sets the text color in CSS."),
            ("What is the correct HTML for a hyperlink?", "<link href='url'>", "<a href='url'>Click</a>", "<a url='url'>Click</a>", "<href='url'>", "B", "Hyperlinks use the <a> tag with the href attribute."),
            ("Which property is used to change the background color?", "bgcolor", "background-color", "color-background", "background", "B", "background-color sets an element's background color in CSS."),
            ("What does JavaScript primarily do?", "Style web pages", "Add interactivity to web pages", "Structure content", "Manage databases", "B", "JavaScript adds behavior and interactivity to web pages."),
            ("Which tag creates an unordered list?", "<ol>", "<list>", "<ul>", "<li>", "C", "<ul> creates an unordered (bulleted) list in HTML."),
            ("What is the CSS box model?", "A 3D model tool", "Content + Padding + Border + Margin", "A JavaScript framework", "A database model", "B", "The box model describes the spacing around HTML elements."),
            ("Which is a JavaScript data type?", "integer", "char", "boolean", "decimal", "C", "boolean (true/false) is a primitive JavaScript data type."),
            ("What does 'responsive design' mean?", "Fast loading pages", "Pages that adapt to screen size", "Pages with animations", "Server-side rendering", "B", "Responsive design ensures websites work on all screen sizes."),
            ("What is a CSS class selector?", "#name", ".name", "*name", "@name", "B", "CSS classes are selected using a period (.) prefix."),
            ("Which HTTP method submits form data?", "GET only", "POST", "PUT", "DELETE", "B", "POST is used to submit form data to a server."),
            ("What is the DOM?", "Document Object Model", "Data Object Manager", "Dynamic Output Mode", "Design Object Method", "A", "The DOM is the browser's representation of an HTML document."),
            ("Which tag is used for inserting images?", "<picture>", "<img>", "<image>", "<src>", "B", "The <img> tag embeds images in HTML pages."),
            ("What is flexbox?", "A JavaScript library", "A CSS layout model", "An HTML5 tag", "A database query", "B", "Flexbox is a CSS layout module for flexible container alignment."),
            ("Which selector has the highest specificity?", "Element selector", "Class selector", "ID selector", "Universal selector", "C", "ID selectors (#id) have higher specificity than class or element selectors."),
            ("What does 'async' do in JavaScript?", "Makes code synchronous", "Makes a function return a Promise", "Loads CSS faster", "Delays execution", "B", "async functions always return a Promise and enable await usage."),
            ("Which is NOT a valid CSS unit?", "px", "em", "dm", "rem", "C", "dm is not a valid CSS unit. px, em, and rem are all valid."),
            ("What is localStorage?", "Server storage", "Browser storage that persists", "Temporary session storage", "Cookie alternative", "B", "localStorage stores data in the browser with no expiration."),
            ("What tag creates a table row?", "<td>", "<th>", "<tr>", "<table>", "C", "<tr> defines a table row in HTML."),
            ("Which event fires when page loads?", "onload", "onready", "onstart", "onopen", "A", "The onload event fires when the page has fully loaded."),
            ("What is CSS Grid?", "A CSS framework", "A 2D layout system", "A JavaScript tool", "A border property", "B", "CSS Grid is a two-dimensional layout system for complex designs."),
            ("What does 'alt' attribute in <img> do?", "Sets image size", "Provides alternative text", "Links the image", "Sets image color", "B", "The alt attribute provides alternative text for screen readers and broken images."),
            ("What is a media query?", "A database query", "A CSS rule for responsive design", "A JavaScript function", "An HTML attribute", "B", "Media queries apply CSS styles based on device characteristics like screen width."),
        ]
    },
    {
        'title': 'Data Science & Analytics',
        'subject': 'Data Science',
        'description': 'Explore data analysis, visualization, statistics, and machine learning fundamentals.',
        'level': 'Intermediate',
        'duration': '10 weeks',
        'icon': '📊',
        'color': '#10b981',
        'questions': [
            ("What does EDA stand for?", "External Data Analysis", "Exploratory Data Analysis", "Extended Data Algorithm", "Evaluated Data Approach", "B", "EDA = Exploratory Data Analysis, the first step in data science."),
            ("Which library is used for data visualization in Python?", "NumPy", "Pandas", "Matplotlib", "SciPy", "C", "Matplotlib is the primary plotting library in Python."),
            ("What is a null hypothesis?", "The proven truth", "The assumption to be tested", "The final conclusion", "A statistical error", "B", "The null hypothesis assumes no significant effect or relationship exists."),
            ("What does 'mean' represent in statistics?", "Middle value", "Most frequent value", "Average value", "Range of values", "C", "The mean is the arithmetic average of all data points."),
            ("What is overfitting in machine learning?", "Model performs well on all data", "Model is too simple", "Model memorizes training data, fails on new data", "Model hasn't been trained", "C", "Overfitting occurs when a model learns noise in training data and fails to generalize."),
            ("Which algorithm is used for classification?", "Linear Regression", "K-Means", "Logistic Regression", "PCA", "C", "Logistic Regression is a classification algorithm despite its name."),
            ("What does pandas DataFrame represent?", "A list structure", "A 2D table-like data structure", "A 1D array", "A dictionary", "B", "A DataFrame is a 2D labeled data structure similar to a spreadsheet."),
            ("What is the purpose of train-test split?", "Speed up training", "Evaluate model on unseen data", "Clean data", "Select features", "B", "Train-test split ensures we evaluate models on data not seen during training."),
            ("What does correlation measure?", "Causation between variables", "Linear relationship strength between variables", "Data variance", "Sample size", "B", "Correlation measures the strength and direction of a linear relationship."),
            ("What is a confusion matrix?", "A visual of neural network layers", "A table showing classification performance", "A data cleaning method", "A normalization technique", "B", "A confusion matrix shows TP, TN, FP, FN counts for classifiers."),
            ("Which measure is resistant to outliers?", "Mean", "Standard deviation", "Median", "Variance", "C", "The median is not affected by extreme outliers like the mean is."),
            ("What is feature engineering?", "Building model architecture", "Creating new features from raw data", "Selecting algorithms", "Evaluating performance", "B", "Feature engineering transforms raw data into meaningful features for models."),
            ("What does PCA stand for?", "Principal Component Analysis", "Predictive Clustering Algorithm", "Partial Correlation Analysis", "Probabilistic Computation Approach", "A", "PCA reduces dimensionality by finding principal components of variance."),
            ("Which regression predicts continuous values?", "Logistic Regression", "Linear Regression", "Decision Tree", "K-Nearest Neighbor", "B", "Linear Regression predicts continuous numerical outputs."),
            ("What is a p-value?", "Probability of data given null hypothesis is true", "Probability hypothesis is true", "Sample size measure", "Effect size", "A", "P-value is the probability of observing results as extreme as those seen, if H0 is true."),
            ("What does RMSE measure?", "Accuracy for classification", "Error magnitude for regression", "Data spread", "Feature importance", "B", "RMSE (Root Mean Square Error) measures average prediction error in regression."),
            ("Which technique prevents overfitting?", "Adding more features", "Regularization", "Removing training data", "Using deeper models", "B", "Regularization adds a penalty term to prevent overfitting."),
            ("What is K-Means clustering?", "A supervised algorithm", "An unsupervised grouping algorithm", "A regression method", "A dimensionality reduction technique", "B", "K-Means is an unsupervised algorithm that groups data into k clusters."),
            ("What is the 80/20 rule in data science?", "80% data collection, 20% analysis", "80% data preparation, 20% modeling", "80% accuracy threshold", "80% training, 20% testing", "B", "Practitioners often spend ~80% of time preparing data and only 20% on modeling."),
            ("What is a random forest?", "A single decision tree", "An ensemble of decision trees", "A neural network layer", "A clustering algorithm", "B", "Random Forest combines multiple decision trees for better accuracy."),
            ("What does 'variance' measure in statistics?", "Central tendency", "Data spread from the mean", "Most common value", "Smallest data point", "B", "Variance measures how spread out data points are from the mean."),
            ("What is cross-validation?", "Testing on training data", "A technique to assess model generalizability", "A normalization method", "A feature selection method", "B", "Cross-validation evaluates model performance using multiple train-test splits."),
            ("Which type of data is age (in years)?", "Nominal", "Ordinal", "Continuous", "Binary", "C", "Age is continuous numerical data with infinite possible values."),
            ("What is the purpose of normalization?", "Remove outliers", "Scale features to a common range", "Increase data size", "Clean missing values", "B", "Normalization scales features so they contribute equally to model training."),
            ("What does ROC curve measure?", "Regression performance", "Classifier performance at various thresholds", "Data distribution", "Training speed", "B", "The ROC curve shows classifier performance across different decision thresholds."),
        ]
    },
    {
        'title': 'Cybersecurity Essentials',
        'subject': 'Cybersecurity',
        'description': 'Learn about network security, encryption, ethical hacking principles, and protecting digital assets.',
        'level': 'Intermediate',
        'duration': '8 weeks',
        'icon': '🔐',
        'color': '#ef4444',
        'questions': [
            ("What does CIA stand for in cybersecurity?", "Central Intelligence Agency", "Confidentiality, Integrity, Availability", "Cyber Intelligence Architecture", "Computer Information Access", "B", "The CIA triad forms the core principles of information security."),
            ("What is phishing?", "A fishing technique", "Deceptive attempts to steal credentials", "A type of malware", "Network monitoring", "B", "Phishing uses deceptive emails/sites to trick users into revealing credentials."),
            ("What is a firewall?", "A physical barrier", "Software/hardware that monitors network traffic", "An antivirus program", "An encryption method", "B", "Firewalls control incoming and outgoing network traffic based on rules."),
            ("What does encryption do?", "Deletes data", "Converts data to unreadable format", "Backs up data", "Compresses data", "B", "Encryption transforms data into ciphertext that only authorized parties can decrypt."),
            ("What is a VPN?", "Virtual Private Network", "Virtual Public Node", "Verified Personal Network", "Variable Private Node", "A", "A VPN creates an encrypted tunnel for secure internet communication."),
            ("What is SQL injection?", "A coding language", "Inserting malicious SQL into queries", "A database backup method", "A login method", "B", "SQL injection attacks insert malicious code into database queries to gain unauthorized access."),
            ("What is two-factor authentication?", "Two passwords", "Identity verification using two different methods", "Two usernames", "Two-step file encryption", "B", "2FA requires two different verification methods, significantly improving security."),
            ("What is a zero-day vulnerability?", "An old bug", "An unknown vulnerability with no available patch", "A network timeout", "A password reset", "B", "Zero-day vulnerabilities are unknown to vendors, making them especially dangerous."),
            ("What does HTTPS stand for?", "HyperText Transfer Protocol Secure", "High Tech Transfer Protocol System", "HyperText Transfer Private System", "Hosted Transfer Protocol Secure", "A", "HTTPS adds TLS/SSL encryption to HTTP for secure communication."),
            ("What is social engineering?", "Building social media apps", "Manipulating people to reveal sensitive info", "Network engineering", "Data engineering", "B", "Social engineering exploits human psychology rather than technical vulnerabilities."),
            ("What is malware?", "Mail software", "Malicious software", "Management software", "Mobile software", "B", "Malware is any software designed to damage, disrupt, or gain unauthorized access."),
            ("What is a brute force attack?", "Physical computer damage", "Trying all possible passwords systematically", "A social engineering attack", "A network flood attack", "B", "Brute force attacks try every possible combination until the correct one is found."),
            ("What is the purpose of SSL/TLS?", "Speed up websites", "Encrypt data in transit", "Store passwords securely", "Block malware", "B", "SSL/TLS protocols encrypt data transmitted between client and server."),
            ("What is ransomware?", "Software that locks data and demands payment", "Antivirus software", "A firewall type", "Network monitoring tool", "A", "Ransomware encrypts victim's files and demands payment for decryption."),
            ("What is penetration testing?", "Testing server speed", "Authorized simulated cyberattack to find vulnerabilities", "Installing patches", "Password recovery", "B", "Pen testing is ethical hacking to identify security weaknesses before attackers do."),
            ("What does GDPR regulate?", "Global data transfer rates", "Personal data protection in Europe", "Government internet access", "Global developer regulations", "B", "GDPR is the EU regulation protecting citizens' personal data and privacy."),
            ("What is a man-in-the-middle attack?", "An insider threat", "Intercepting communication between two parties", "A password attack", "A DDoS variant", "B", "MITM attacks intercept and potentially alter communication between two parties."),
            ("What is the principle of least privilege?", "Give users minimum necessary access", "Give all users admin access", "No access for new users", "Equal access for all", "A", "Least privilege limits user access rights to the minimum needed for their role."),
            ("What is a digital certificate?", "An offline credential", "A digital document verifying identity", "An encrypted file", "A firewall rule", "B", "Digital certificates are electronic credentials that verify identity online."),
            ("What does DDoS stand for?", "Distributed Denial of Service", "Dynamic Data over Service", "Direct Denial of Security", "Distributed Data on Systems", "A", "DDoS attacks overwhelm servers with traffic from multiple sources."),
            ("What is biometric authentication?", "Password authentication", "Identity verification using physical characteristics", "Two-factor authentication", "Token authentication", "B", "Biometric authentication uses fingerprints, face, or other physical traits."),
            ("What is a honeypot in cybersecurity?", "Sweet encrypted data", "A decoy system to attract attackers", "A secure server", "An antivirus trap", "B", "Honeypots are decoy systems designed to detect and study attackers."),
            ("What is cryptography?", "Writing secret messages by hand", "Science of secure communication using codes", "Computer programming", "Data compression", "B", "Cryptography uses mathematical algorithms to secure information."),
            ("What does IAM stand for?", "Internet Access Management", "Identity and Access Management", "Internal Application Monitoring", "Integrated Authentication Method", "B", "IAM frameworks manage digital identities and control resource access."),
            ("Which is a strong password practice?", "Using your name", "Using the same password everywhere", "Using 12+ character mix of letters, numbers, symbols", "Writing password on paper", "C", "Strong passwords are long, complex, unique, and stored in a password manager."),
        ]
    },
]

print("Seeding database...")

for cd in courses_data:
    questions_data = cd.pop('questions')
    course, created = Course.objects.get_or_create(
        title=cd['title'],
        defaults=cd
    )
    if created:
        print(f"  Created course: {course.title}")
    else:
        print(f"  Course exists: {course.title}")
        # Update fields
        for k, v in cd.items():
            setattr(course, k, v)
        course.save()

    # Delete existing questions and recreate
    course.questions.all().delete()
    for q in questions_data:
        Question.objects.create(
            course=course,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_answer=q[5],
            explanation=q[6],
        )
    print(f"    Added {len(questions_data)} questions")

print("\n✅ Database seeded successfully!")
print("You can now run: python manage.py runserver")
