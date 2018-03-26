from django.db import models

from .models import Inspector, Notes
from apps.projects.models import Project
from apps.invoices.models import Invoice
from apps.partners.models import LetProject, PlannedProject
from datetime import date, datetime, timedelta
from apps.utils.helpers import formatted_date, last_sunday, next_sunday

def check_planned_projects(office):
    planned_projects = '''<h2> Coming soon to a city near you:</h2>'''

    for project in PlannedProject.objects.filter(office=office).filter(scrapped_date=PlannedProject.objects.latest('scrapped_date')):
        planned_projects += f'''<strong><p>
        {project.name}(<a href={project.url}>{project.agreement_number}</a>):</p></strong>
        <br/>
        <p>Cost: {project.cost}</p>
        <p>Anticipated Advance: {advance_date}</p>
        <br>
        <p>{description}</p>'''

    if len(planned_projects) > 65:
        return planned_projects
    return ''

def check_inspector_certs(office):
    ''' For each inspector, if they have a certain certification, make suer the expiration date isn't within the next 90 days '''
    future_date = date.today() + timedelta(days=90)
    cert_html = '''<h2> Inspector Updates </h2>'''
    for inspector in Inspector.objects.filter(office=office):
        if inspector.nicet_expiration:
            if inspector.nicet_expiration < future_date:
                cert_html += f'''<li>{inspector.first_name} {inspector.last_name}'s NICET expires {formatted_date(inspector.nicet_expiration)}</li>'''
        if inspector.penndot_bituminous:
            if inspector.penndot_bituminous < future_date:
                cert_html += f'''<li>{inspector.first_name} {inspector.last_name}'s PennDOT Bituminous expires {formatted_date(inspector.penndot_bituminous)}</li>'''
        if inspector.necept_bituminous:
            if inspector.necept_bituminous < future_date:
                cert_html += f'''<li>{inspector.first_name} {inspector.last_name}'s NECEPT Bituminous expires {formatted_date(inspector.necept_bituminous)}</li>'''
        if inspector.penndot_concrete:
            if inspector.penndot_concrete < future_date:
                cert_html += f'''<li>{inspector.first_name} {inspector.last_name}'s PennDOT Concrete expires {formatted_date(inspector.penndot_concrete)}</li>'''
        if inspector.aci_concrete:
            if inspector.aci_concrete < future_date:
                cert_html += f'''<li>{inspector.first_name} {inspector.last_name}'s ACI Concrete expires {formatted_date(inspector.aci_concrete)}</li>'''
    if len(cert_html) > 30:
        cert_html += '''<p>inspector certs can be updated <a href='Prudentrlawson.pythonanywhere.com/inspectors/update'>here</a>.</p>'''
        return cert_html
    return ''

def check_invoice_created(office):
    ''' See if anything is new this week in invoices

        Invoices are done once a month, so we check if the last sunday of the
        month has happened yet. If it has we list the invoices that need updating.
     '''
    # last sunday wasn't the last sunday of the month, don't run this.
    if datetime.now() - timedelta(days=21) == (next_sunday().month):
        return ''
    new_invoice_html = '''<h2> This Week in Invoices </h2>'''

    for project in Project.objects.filter(office=office).filter(active=True):
        new_invoice_html += f'''<p>{project.penndot_number} needs to be invoiced from {formatted_date(project.get_last_invoiced())} to
        {formatted_date(last_sunday())} </p>'''

    new_invoice_html += '''<p font-size:8px>
    Invoice data can be added at <a href='https://www.prudentrlawson.pythonanywhere.com/projects/invoices/update'>here</a>.
    <br/> 
    Projects can be set to inactive <a href='https://www.prudentrlawson.pythonanywhere.com/projects/update'>here</a>.
    </p>'''
    return new_invoice_html

def check_invoice_reviewed(office):
    '''
    If an invoice is logged, but has no invoice number, we see if it was
    forgotten or if syracuse has to be hit up
    '''
    recent_date = datetime.now() + timedelta(days=7)
    reviewed_invoice = "<h2>Pending Invoices</h2>"

    for invoice in Invoice.objects.filter(last_modified__lte=recent_date).filter(status__lte=2):
        if not invoice.invoice_number:
            reviewed_invoice += f'''<p> I'm missing an invoice number for {invoice.project.prudent_number} #{invoice.estimate_number}, which is currently
            {invoice.readable_status}</p>'''

    if len(reviewed_invoice) > 30:
        reviewed_invoice += '''<p>Invoice numbers can be added <a href='Prudentrlawson.pythonanywhere.com/invoices/update'>here</a>.</p>'''
        return reviewed_invoice

    return ''

def check_project_burnrate(office):
    '''
    See if any projects are like to run out of money soon
    '''
    burn_notice = '''<h2>Budgets Approaching:</h2>'''
    for project in Project.objects.filter(office=office).filter(active=True):
        # Get the average amount of the last 3 invoices' labor cost
        last_3_avg = project.invoice_set.order_by("-id")[:3].aggregate(models.Avg('labor_cost'))
        burn_rate = list(last_3_avg.values())[0]
        # if there aren't any invoices to use to create a burn rate, then set
        # the burn rate to one so the whole thing doesn't fail.
        if burn_rate is None:
            burn_rate = 1
        months_left = round((float(project.payroll_budget) - project.payroll_to_date)/burn_rate)
        if months_left <= 3:
            end_project = formatted_date(project.get_last_invoiced() + timedelta(days=(months_left*30)))
            burn_notice += f'''<p>{project.prudent_number} projects to reach it's payroll budget by {end_project}</p>'''

        last_3_avg = project.invoice_set.order_by("-id")[:3].aggregate(models.Avg('other_cost'))
        burn_rate = list(last_3_avg.values())[0]
        if burn_rate is None:
            burn_rate = 1
        months_left = round((float(project.other_cost_budget) - project.other_cost_to_date)/burn_rate)
        if months_left <= 3:
            burn_notice += f'''<p>{project.prudent_number} projects to reach it's other cost budget by {formatted_date(project.get_last_invoiced() + timedelta(days=(months_left*30)))}</p>'''
    if len(burn_notice) > 70:
        return burn_notice

    return ''
