from django import forms

from clac.models import Showcase


class ShowcaseForm(forms.ModelForm):
    class Meta:
        model = Showcase
        fields = ["title", "body_md"]

    def clean_body_md(self):
        body_md = self.cleaned_data["body_md"]
        if len(body_md.strip().split()) < 5:
            raise forms.ValidationError("Body must be at least 5 words long.")
        return body_md


# ✅ tests.py (only the fixed section shown)


class ShowcaseFormTest(forms.ModelForm):
    class Meta:
        model = Showcase
        fields = ["title", "body_md"]

    def clean_body_md(self):
        body_md = self.cleaned_data["body_md"]
        if len(body_md.strip().split()) < 5:
            raise forms.ValidationError("Body must be at least 5 words long.")
        return body_md
