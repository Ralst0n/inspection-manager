from datetime import datetime

import string

from django.contrib.auth.models import User
from django.core import mail
from django.utils.crypto import get_random_string

from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from inspectors.newsletters import (
    check_inspector_certs, check_invoice_created, check_invoice_reviewed,
    check_project_burnrate
)
from partners.models import LetProject, PlannedProject
from utils.planned_project_scraper import PlannedProjectScraper
from utils.let_project_scraper import LetProjectScrapper

@periodic_task(
    run_every=crontab(minute='*/3'),
    name='scrape_let_projects',
    ignore_result=True
)
def scrape_let_projects():
    p = LetProjectScrapper()
    p.run()
    return "Mission Complete!"

@periodic_task(
    run_every=crontab(minute='*/3'),
    name='scrape_planned_projects',
    ignore_result=True
)
def scrape_planned_projects():
    return 'c'
    p = PlannedProjectScraper()
    scraped_projects = p.run()
    if not scraped_projects:
        return "Nothing to see here."
    for project in scraped_projects:
        PlannedProject.objects.create(
        district=project[0],
        agreement_number=project[1],
        name=project[2],
        advance_date=project[3],
        cost=project[4],
        url=project[5],
        office=project[6],
        description=project[7]
        )

@periodic_task(
    run_every=crontab(minute='*/5'),
    name='email_news_letter',
    ignore_result=True
)
def email_news_letter(office='King of Prussia'):
    # makes datetime format as `<month name> <day>`
    date = datetime.now().strftime('%B %d')
    subject = f'{office}: Week of {date}'
    message =''
    message += check_inspector_certs(office)
    message += check_invoice_created(office)
    message += check_invoice_reviewed(office)
    message += check_project_burnrate(office)
    if not message:
        message += "Nothing to work on this week."
    return message[:140]
    mail.send_mail(
        subject,
        message,
        'noreply@officeassistant.com',
        ['rlawson@prudenteng.com',],
        fail_silently=False,
        html_message=message,
    )
    return message[:140]
