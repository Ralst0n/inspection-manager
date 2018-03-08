from django import forms

from .models import Comments, Invoice

class InvoiceCreationForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('name', 'invoice_file',)


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