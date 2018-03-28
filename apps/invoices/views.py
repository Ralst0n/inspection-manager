from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CommentCreationEditForm, CommentCreationForm, InvoiceCompletionForm, InvoiceCreationForm
from .models import Invoice, Comments
from apps.profiles.models import Profile

class InvoiceList(ListView):
    def get_queryset(self):
        # People of the office should only see their invoices that are not yet approved
        if self.request.user.profile.role == "Preparer" or self.request.user.profile.role == "Manager":
            queryset = Invoice.objects.filter(status__lte=2).filter(project__office=self.request.user.profile.office)

        # Reviewers should only see invoices that are currently in their queue
        elif self.request.user.profile.role == "Reviewer":
            queryset = Invoice.objects.filter(status=2)
        elif self.request.user.profile.role == "Observer":
            queryset = Invoice.objects.all()
            
        return queryset
    template_name = "templates/invoice_list.html"
    # Set the name to be used in the template to access object list
    context_object_name = "invoices"

class InvoiceView(LoginRequiredMixin, DetailView):
    model = Invoice

    template_name = 'details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(invoice=self.object).order_by('-created_at')
        return context


def invoice_new(request):
    if request.method == "POST":
        invoice_form = InvoiceCreationForm(request.POST, request.FILES)
        comment_form = CommentCreationForm(request.POST)
        if invoice_form.is_valid() and comment_form.is_valid():
            invoice = invoice_form.save(commit=False)
            comment = comment_form.save(commit=False)
            invoice.creator = request.user
            invoice.created_at = timezone.now()
            invoice.save()

            comment.body = f"[Invoice Created] {comment.body}"
            comment.creator = request.user
            comment.created_at = timezone.now()
            comment.invoice = invoice
            comment.save()
            return redirect('invoices:details', pk=invoice.id)
        return render(request, 'templates/invoice_create.html', {'invoice_form':invoice_form,
        'comment_form': comment_form })
    else:
        invoice_form = InvoiceCreationForm()
        comment_form = CommentCreationForm()
        return render(request, 'templates/invoice_create.html', {'invoice_form':invoice_form,
        'comment_form': comment_form })

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = InvoiceCreationForm(request.POST, request.FILES, instance=invoice)
        comment_form = CommentCreationEditForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=True)
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.created_at = timezone.now()
            comment.body = f"[Edit] {comment.body}"
            comment.invoice = invoice
            comment.save()
            return redirect('invoices:details', pk=pk)
    else:
        form = InvoiceCreationForm(instance=invoice)
        comment_form = CommentCreationEditForm()
    return render(request, 'templates/invoice_create.html', {'invoice_form': form, 'invoice':invoice, 'edit': True,
     'comment_form':comment_form})

def invoice_submit(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    if invoice:
        if invoice.status == 0:
            # if an invoice is submitted from draft send an email to the
            # manager notifying them the invoice is available for review
            messages.add_message(request, messages.INFO, f"Invoice Sumbitted to Management!")
            recip_set = Profile.objects.filter(office=invoice.creator.profile.office).filter(role="Manager")
            recipients = []
            for recipient in recip_set:
                recipients.append(recipient.user.email)
            emessage = f"<p>{invoice.creator.first_name} {invoice.creator.last_name} has submitted <a href=localhost:8000/invoices/{pk}> {invoice.name}</a> for your approval.</p>"
            send_mail(
                f" Invoice Review: {invoice.name}",
                '',
                'Prudent Invoicer',
                recipients,
                fail_silently=False,
                html_message=emessage
            )
        elif invoice.status == 1:
            # if an invoice is submitted by a Manager
            messages.add_message(request, messages.INFO, f"Invoice Approved for Final Review!")
            # Add a comment to the Invoice Showing who approved it
            comment = Comments()
            comment.body = f"{request.user.profile.role} Approved"
            comment.creator = request.user
            comment.created_at = timezone.now()
            comment.invoice = invoice
            comment.save()
        else:
            # Notify both preparer and manager that an invoice is prepared for ECMS
            messages.add_message(request, messages.INFO, f"Invoice Approved for Submission")
            recip_set = Profile.objects.filter(office=invoice.creator.profile.office).filter(
                 Q(role="Manager") | Q(role="Preparer")
            )
            recipients = []
            for recipient in recip_set:
                recipients.append(recipient.user.email)
            emessage = f'''<p>{request.user.get_full_name()} 
            approved {invoice.name}
            for ECMS submission! The invoice is #{invoice.invoice_number}'''
            send_mail(
                f" Invoice Review: {invoice.name}",
                '',
                'Prudent Invoicer',
                recipients,
                fail_silently=False,
                html_message=emessage
            )
            # Add a comment to the Invoice Showing who approved it
            comment = Comment()
            comment.body = f"{request.user.profile.role} Approved"
            comment.creator = request.user
            comment.created_at = timezone.now()
            comment.invoice = invoice
            comment.save()
        if invoice.status < 3:
            invoice.status = invoice.status + 1
        invoice.save()
    return redirect('invoices:details', pk=pk)

def invoice_reject(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = CommentCreationEditForm(request.POST)
        if form.is_valid():
            if invoice.status > 0:
                invoice.status = invoice.status - 1
                messages.add_message(request, messages.INFO, f"Invoice Status revereted to {invoice.STATUS_CODE[invoice.status][1]}")
            invoice.save()
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.created_at = timezone.now()
            comment.body = f"[Reject] {comment.body}"
            comment.invoice = invoice
            comment.save()
            return redirect('invoices:details', pk=pk)
    else:
        form = InvoiceCreationForm(instance=invoice)
        comment_form = CommentCreationEditForm()
    return render(request, 'templates/invoice_reject.html',
        {
        'invoice':invoice,
        'edit': True,
        'comment_form':comment_form,
        }
    )

def invoice_number(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = InvoiceCompletionForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice.save()
            return redirect('invoices:details', pk=pk)
    else:
        form = InvoiceCompletionForm(instance=invoice)
        return render(request, 'templates/invoice_number.html', {'form': form, 'invoice': invoice})