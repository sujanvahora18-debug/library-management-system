from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Book, Borrow, Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "available_copies"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "available_copies": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 3}),
        }

    def clean_available_copies(self):
        value = self.cleaned_data["available_copies"]
        if value < 0 or value > 3:
            raise forms.ValidationError("Available copies must be between 0 and 3.")
        return value


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["full_name", "email", "phone", "address", "joined_at"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "joined_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class IssueBookForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    book = forms.ModelChoiceField(queryset=Book.objects.filter(available_copies__gt=0), widget=forms.Select(attrs={"class": "form-control"}))
    borrow_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        borrow_date = cleaned_data.get("borrow_date")
        if borrow_date:
            if borrow_date > timezone.localdate():
                raise forms.ValidationError("Borrow date cannot be in the future.")
            cleaned_data["due_date"] = borrow_date + timedelta(days=7)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["member"].queryset = Member.objects.all()
        self.fields["book"].queryset = Book.objects.filter(available_copies__gt=0)


class ReturnBookForm(forms.Form):
    borrow = forms.ModelChoiceField(
        queryset=Borrow.objects.filter(return_date__isnull=True).select_related("member", "book"),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Active Borrow",
    )
    return_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["borrow"].queryset = Borrow.objects.filter(return_date__isnull=True).select_related("member", "book")

    def clean(self):
        cleaned_data = super().clean()
        borrow = cleaned_data.get("borrow")
        return_date = cleaned_data.get("return_date")
        if borrow and return_date and return_date < borrow.borrow_date:
            raise forms.ValidationError("Return date cannot be earlier than borrow date.")
        return cleaned_data
