from django import forms
from .models import ConversationMessage
from django.core.exceptions import ValidationError
import re

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        labels = {
            'content': '',  # Remove the label for the 'content' field
        }
        widgets = {
            'content':forms.Textarea(attrs={
                'class':'w-full  p-2   rounded-3xl border',
                'rows':2,
                'cols':50,
                'placeholder':'Your text goes here...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise ValidationError("Message content cannot be empty.")
        if len(content) > 1000:
            raise ValidationError("Message content cannot exceed 1000 characters.")
        # Basic sanitization: remove potential script tags
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        # Remove other potentially harmful tags
        content = re.sub(r'<[^>]+>', '', content)
        return content
