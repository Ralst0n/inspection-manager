from django.test import TestCase
from projects.models import Project, Invoice
from inspectors.models import Inspector
from datetime import date
from django.core import mail
# Create your tests here.
from inspectors.tasks import email_news_letter
from inspectors.newsletters import (
    check_inspector_certs, check_invoice_created, check_invoice_reviewed,
    check_project_burnrate
)

class NewsletterTestCase(TestCase):
    def setUp(self):
        I1 = Inspector.objects.create(
            first_name = "Mark",
            last_name = "Test",
            office = "King of Prussia",
            classification = "TCI-2",
            address ="123 kitty lane",
            location = "Pittsburgh, PA",
            work_radius = 95,
            email = "marktest@prudenteng.com",
            phone_number = "3022993322",
        )
        self.p1= Project.objects.create(
            prudent_number='1',
            penndot_number='1',
            office ='King of Prussia',
            name='tester1',
            start_date= date.today(),
            end_date=date.today(),
            inspector='',

        )

    # def test_inspector_certs(self):
    #     self.assertEqual(check_inspector_certs("King of Prussia"), '')

    # def test_invoice_created(self):
    #     self.assertEqual(check_invoice_created("King of Prussia"), '')

    def test_invoice_reviewed(self):
        self.assertEqual(check_invoice_reviewed("King of Prussia"), '')

    def test_project_burnrate(self):
        self.assertEqual(check_project_burnrate("King of Prussia"), '')

    # def test_payroll_to_date(self):
    #     print(self.p1.payroll_budget)
    #     print(type(self.p1.payroll_budget))
    #     print(self.p1.payroll_to_date)
    #     print(type(self.p1.payroll_to_date))


    # def test_send_email(self):
    #     subject, message = email_news_letter()
    #     mail.send_mail(
    #         subject, message,
    #         'from@example.com', ['to@example.com'],
    #         fail_silently=False,
    #     )
    #
    #     # Test that one message has been sent.
    #     self.assertEqual(len(mail.outbox), 1)
    #
    #     # Verify that the subject of the first message is correct.
    #     self.assertEqual(mail.outbox[0].subject, 'Subject here')
