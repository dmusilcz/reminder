from django_cron import CronJobBase, Schedule
from django.conf import settings
from main.models import ReminderThrough
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail, get_connection, EmailMultiAlternatives
from datetime import timedelta
from collections import defaultdict
from django.utils.translation import activate
from django.template.loader import render_to_string


class SendReminders(CronJobBase):
    # RUN_EVERY_MINS = 0.2
    RUN_AT_TIMES = ['5:00']
    MIN_NUM_FAILURES = 2

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'send_reminders'

    def do(self):
        try:
            today = timezone.localdate()
            reminder_throughs = ReminderThrough.objects.all()

            docs_reminder_sent_today = [(reminder.document, str(reminder.get_days_by_id())) for reminder in reminder_throughs if reminder.document.expiry_date - timedelta(days=reminder.get_days_by_id()) == today]
            print(docs_reminder_sent_today)

            users = defaultdict(list)

            for doc_reminder in docs_reminder_sent_today:
                users[doc_reminder[0].author].append((doc_reminder[0].name, doc_reminder[0].expiry_date, doc_reminder[1]))
                doc_reminder[0].last_reminder_sent = timezone.localtime()
                doc_reminder[0].save()

            email_records = list()

            for user, document_info in users.items():
                email_record = self.compose_email_for_user(user, document_info)
                email_records.append(email_record)

            email_records = tuple(email_records)

            emails_sent = self.send_mass_html_mail(email_records)
            print(f'Reminder emails sent today: {emails_sent}')

        except Exception as e:
            print(e)

    def compose_email_for_user(self, user, document_info):
        language = user.profile.language
        activate(language)

        text = render_to_string('main/reminder_email_plain.html', {'username': user.username,
                                                             'document_info': document_info})
        html = render_to_string('main/reminder_email.html', {'username': user.username,
                                                             'document_info': document_info})

        return (settings.EMAIL_SUBJECT_PREFIX, text, html, settings.DEFAULT_FROM_EMAIL, [user.email,])

    def send_mass_html_mail(self, datatuple, fail_silently=False, user=None, password=None, connection=None):
        """
        Given a datatuple of (subject, text_content, html_content, from_email,
        recipient_list), sends each message to each recipient list. Returns the
        number of emails sent.

        If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
        If auth_user and auth_password are set, they're used to log in.
        If auth_user is None, the EMAIL_HOST_USER setting is used.
        If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

        """
        connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
        messages = []

        for subject, text, html, from_email, recipient in datatuple:
            message = EmailMultiAlternatives(subject, text, from_email, recipient, headers={'List-Unsubscribe': '<https://www.neverexpire.net/docs/>'})
            message.attach_alternative(html, 'text/html')
            messages.append(message)

        return connection.send_messages(messages)
