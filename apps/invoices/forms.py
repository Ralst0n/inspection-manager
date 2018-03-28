from django import forms

from .models import Comments, Invoice

class InvoiceCreationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('project', 'estimate_number', 'start_date', 'end_date', 
            'labor_cost', 'other_cost', 'straight_hours', 'overtime_hours',
             'invoice_file')


class CommentCreationForm(forms.ModelForm):
    body = forms.CharField(
        label='', 
        max_length=280, 
        required=False,
        widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('body',)
class CommentCreationEditForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ('body',)

class InvoiceCompletionForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('invoice_number',)