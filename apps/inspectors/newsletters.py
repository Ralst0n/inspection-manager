from django.db import models
from decimal import Decimal

from .models import Inspector, Notes
from apps.projects.models import Project
from apps.invoices.models import Invoice
from apps.partners.models import LetProject, PlannedProject
from datetime import date, datetime, timedelta
from apps.utils.helpers import formatted_date, last_sunday, next_sunday, last_last_sunday, months_last_sunday

def check_planned_projects(office):
    planned_projects = '''<h2> Coming Soon to a City Near You</h2>'''
    # Get last successful scrapped date
    latest_scrape = PlannedProject.objects.latest("scrapped_date").scrapped_date
    # Add data for each project found since the last successful scrape
    for project in PlannedProject.objects.filter(office=office).filter(scrapped_date__gt=latest_scrape):
        planned_projects += f'''<strong><p>
        {project.name}(<a href={project.url}>{project.agreement_number}</a>):</p></strong>

        <p>District: {project.district}</p>

        <p>Cost: {project.cost}</p>
        <p>Anticipated Advance: {project.advance_date}</p>

        <p>{project.description}</p>'''

    if len(planned_projects) > 65:
        return planned_projects
    return ''

def check_inspector_certs(office):
    ''' For each inspector, if they have a certain certification, make suer the expiration date isn't within the next 90 days '''
    future_date = date.today() + timedelta(days=90)
    cert_html = '''<h2> Inspector Updates</h2>'''
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
        cert_html += '''<p>inspector certs can be updated <a href='https://prudentoffice.herokuapp.com/inspectors/'>here</a>.</p>'''
        return cert_html
    return ''

def check_invoice_created(office):
    ''' See if anything is new this week in invoices

        Invoices are done once a month, so we check if the last sunday of the
        month has happened yet. If it has we list the invoices that need updating.
     '''
    new_invoice_html = '''<h2> This Week's Invoices</h2>'''

    for project in Project.objects.filter(office=office).filter(active=True):
        # if the last invoiced date for the project is older than 
        # the most recent `invoicing date`
        if datetime.strptime(project.last_invoiced, "%m/%d/%Y") < last_last_sunday():
            # needs to be invoiced from last invoice date + 1 day to most recent invoice date
            new_invoice_html += f'''<p>{project.penndot_number} needs to be invoiced from {formatted_date(project.get_last_invoiced() +timedelta(days=1))} to
            {formatted_date(last_last_sunday())} </p>'''

    new_invoice_html += '''<p font-size:8px>
    Invoice data can be added at <a href='https://prudentoffice.herokuapp.com/invoices'>here</a>.
    <br/> 
    Projects can be set to inactive <a href='https://prudentoffice.herokuapp.com/projects'>here</a>.
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
            reviewed_invoice += f'''<p> Invoice {invoice.project.prudent_number} #{invoice.estimate_number}, was placed into 
            {invoice.readable_status} status on {formatted_date(invoice.last_modified)}</p>'''

    if len(reviewed_invoice) > 30:
        reviewed_invoice += '''<p>Invoices can be approved <a href='https://prudentoffice.herokuapp.com/invoices'>here</a>.</p>'''
        return reviewed_invoice

    return ''

def check_project_burnrate(office):
    '''
    See if any projects are like to run out of money soon
    '''
    burn_notice = '''<h2>Budgets Approaching</h2>'''
    for project in Project.objects.filter(office=office).filter(active=True):
        # Get the average amount of the last 3 invoices' labor cost
        invoice_set =  project.invoice_set.order_by("-end_date")[:3]
        # If there are no invoices, end this check
        if invoice_set.count() == 0:
            return ""
        # Get the total labor cost of last 3 invoices as a decimal
        last_3 = project.invoice_set.order_by("-end_date")[:3].aggregate(models.Sum('labor_cost'))
        # Get just the Decimal value from last_3
        burn_rate = list(last_3.values())[0]
        total_duration = 0        
        for invoice in invoice_set:
             total_duration += (invoice.end_date - invoice.start_date).days
        
        daily_avg = Decimal(burn_rate / total_duration)
        days_left = round(((project.payroll_budget) - project.payroll_to_date)/daily_avg)
        if days_left <= 120:
            end_project = formatted_date(project.get_last_invoiced() + timedelta(days=(days_left)))
            burn_notice += f'''<p><strong>{project.prudent_number}</strong> projects to reach it's payroll budget by <strong>{end_project}</strong></p>'''
        
        # Repeat process for other cost 
        last_3 = project.invoice_set.order_by("-end_date")[:3].aggregate(models.Sum('other_cost'))
        burn_rate = list(last_3.values())[0]
        daily_avg = Decimal(burn_rate / total_duration)
        days_left = round((project.other_cost_budget - project.other_cost_to_date)/daily_avg)
        if days_left <= 120:
            end_project = formatted_date(project.get_last_invoiced() + timedelta(days=(days_left)))
            burn_notice += f'''<p><strong>{project.prudent_number}</strong> projects to reach it's other cost budget by <strong>{end_project}</strong></p>'''
    if len(burn_notice) > 70:
        return burn_notice

    return ''
