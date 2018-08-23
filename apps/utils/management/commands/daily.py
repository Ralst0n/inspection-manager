from django.core.management.base import BaseCommand, CommandError

from rq import Queue
from worker import conn
from apps.inspectors.tasks import scrape_let_projects, scrape_planned_projects

class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Queue(connection=conn)
        q.enqueue(scrape_let_projects)
        q.enqueue(scrape_planned_projects)