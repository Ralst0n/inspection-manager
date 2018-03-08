from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CommentCreationEditForm, CommentCreationForm, InvoiceCreationForm
from .models import Invoice, Comments
from apps.profiles.models import Profile

class InvoiceList(ListView):
    def get_queryset(self):
        if self.request.user.profile.role is "Preparer" or self.request.user.profile.role is "Manager":
            queryset = Invoice.objects.filter(creator.user.profile.office==request.user.profile.office)

        else:
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
            messages.add_message(request, messages.INFO, f"Invoice Sumbitted to Management!")
            emessage = f"<p><a href=localhost:8000/invoices/{pk}>{invoice.name}</a> has been submitted.</p>"
            send_mail(
                f" Invoice Review: {invoice.name}",
                '',
                'Prudent Invoicer',
                ['rlawson@prudenteng.com'],
                fail_silently=False,
                html_message=emessage
            )
        elif invoice.status == 1:
            messages.add_message(request, messages.INFO, f"Invoice Approved for Final Review!")
        else:
             messages.add_message(request, messages.INFO, f"Invoice Approved for Final Review!")
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
