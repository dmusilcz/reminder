from django.test import TestCase

from django.core import mail
from django.urls import reverse
from django.test import TestCase
from .models import Document, ReminderChoice, Category
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo
from django.contrib.auth.models import User

class EmailTest(TestCase):
    def test_email_sent(self):
        user = User.objects.create(username='Tester')
        reminder_choice = ReminderChoice.objects.create(author=user, field='1 day')
        doc = Document.objects.create(name='Test', author=user, expiry_date=timezone.localdate()-timedelta(days=2))
        doc.reminder.set([reminder_choice])
        print(doc.expiry_date)
        today = timezone.localdate()
        print(doc.expiry_date < today)
        body = 'This is a test message'
        mail.send_mail('Hello', body, 'noreply@mysite.com', ['test@example.com', ])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, 'This is a test message')