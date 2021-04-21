from django.core.exceptions import ValidationError
from encyclopedia.util import get_entry, list_entries
from typing import Any, Dict
from django import forms


class NewEntryFrom(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(widget=forms.Textarea)

    def clean(self) -> Dict[str, Any]:
        if self.cleaned_data.get("title") in list_entries():
            raise ValidationError(f"Entry {self.cleaned_data.get('title')} already exists")
        return super().clean()

class EditEntryFrom(NewEntryFrom):
    def clean(self) -> Dict[str, Any]:
        pass