from django.test import TestCase

from django.core import mail
from django.urls import reverse
from django.test import TestCase
from .models import Document, ReminderChoice, Category
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo
from django.contrib.auth.models import User

import re
from django.urls import reverse, NoReverseMatch
from django.test import TestCase, Client
from django.core import mail
from django.test.utils import override_settings
from django.contrib.auth import authenticate

# class EmailTest(TestCase):
#     def test_email_sent(self):
#         user = User.objects.create(username='Tester')
#         reminder_choice = ReminderChoice.objects.create(author=user, field='1 day')
#         doc = Document.objects.create(name='Test', author=user, expiry_date=timezone.localdate()-timedelta(days=2))
#         doc.reminder.set([reminder_choice])
#         print(doc.expiry_date)
#         today = timezone.localdate()
#         print(doc.expiry_date < today)
#         body = 'This is a test message'
#         mail.send_mail('Hello', body, 'noreply@mysite.com', ['test@example.com', ])
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].body, 'This is a test message')

VALID_USER_NAME = "username"
USER_OLD_PSW = "oldpassword"
USER_NEW_PSW = "newpassword"
PASSWORD_RESET_URL = reverse("app:password_reset")

def PASSWORD_RESET_CONFIRM_URL(uidb64, token):
    try:
        return reverse("app:password_reset_confirm", args=(uidb64, token))
    except NoReverseMatch:
        return f"/accounts/reset/invaliduidb64/invalid-token/"


def utils_extract_reset_tokens(full_url):
    return re.findall(r"/([\w\-]+)",
                      re.search(r"^http\://.+$", full_url, flags=re.MULTILINE)[0])[3:5]


@override_settings(EMAIL_BACKEND="anymail.backends.test.EmailBackend")
class PasswordResetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.myclient = Client()

    def test_password_reset_ok(self):
        # ask for password reset
        response = self.myclient.post(PASSWORD_RESET_URL,
                                      {"email": VALID_USER_NAME},
                                      follow=True)

        # extract reset token from email
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        uidb64, token = utils_extract_reset_tokens(msg.body)

        # change the password
        response = self.myclient.post(PASSWORD_RESET_CONFIRM_URL(uidb64, token),
                                      {"new_password1": USER_NEW_PSW,
                                       "new_password2": USER_NEW_PSW},
                                      follow=True)

        self.assertIsNone(authenticate(username=VALID_USER_NAME,password=USER_OLD_PSW))