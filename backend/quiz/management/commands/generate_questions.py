from django.core.management.base import BaseCommand
from quiz.models import Question  # Replace 'quiz' with your app name if different


class Command(BaseCommand):
    help = 'Generate quiz questions related to SQL, React.js, Django, and Python'

    def handle(self, *args, **kwargs):
        questions = [
            # SQL Questions
            {
                'text': "What does the SQL command 'SELECT' do?",
                'option_a': "Deletes records",
                'option_b': "Updates records",
                'option_c': "Retrieves data from a table",
                'option_d': "Adds new records to a table",
                'correct_answer': 'c',
            },
            {
                'text': "Which SQL keyword is used to sort the result-set?",
                'option_a': "SORT BY",
                'option_b': "ORDER BY",
                'option_c': "GROUP BY",
                'option_d': "FILTER BY",
                'correct_answer': 'b',
            },
            # React.js Questions
            {
                'text': "What is the purpose of React's useState hook?",
                'option_a': "To manage state in functional components",
                'option_b': "To handle HTTP requests",
                'option_c': "To optimize performance",
                'option_d': "To define routes",
                'correct_answer': 'a',
            },
            {
                'text': "What is the virtual DOM in React?",
                'option_a': "A lightweight copy of the real DOM",
                'option_b': "A database for storing components",
                'option_c': "A package manager for React apps",
                'option_d': "A debugging tool",
                'correct_answer': 'a',
            },
            # Django Questions
            {
                'text': "Which of these is used to define a URL pattern in Django?",
                'option_a': "views.py",
                'option_b': "models.py",
                'option_c': "urls.py",
                'option_d': "settings.py",
                'correct_answer': 'c',
            },
            {
                'text': "What is the purpose of Django's ORM?",
                'option_a': "To manage static files",
                'option_b': "To execute SQL queries",
                'option_c': "To map database tables to Python objects",
                'option_d': "To define middleware",
                'correct_answer': 'c',
            },
            # Python Questions
            {
                'text': "What is the output of 'print(2 ** 3)' in Python?",
                'option_a': "5",
                'option_b': "8",
                'option_c': "6",
                'option_d': "9",
                'correct_answer': 'b',
            },
            {
                'text': "Which of these is NOT a Python data type?",
                'option_a': "list",
                'option_b': "integer",
                'option_c': "array",
                'option_d': "tuple",
                'correct_answer': 'c',
            },
        ]

        for question_data in questions:
            question, created = Question.objects.get_or_create(**question_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Question added: {question.text[:50]}"))
            else:
                self.stdout.write(self.style.WARNING(f"Question already exists: {question.text[:50]}"))

        self.stdout.write(self.style.SUCCESS("Questions generated successfully!"))
