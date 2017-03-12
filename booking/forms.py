from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit
from django import forms
from django.conf import settings
from members.models import Structure
from .models import Booking, BookingState


# TODO: add a reinit button
# TODO: use https://behigh.github.io/bootstrap_dropdowns_enhancement
class BookingFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].initial = settings.NOW().year
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field_with_label.html'
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            'structure',
            'year',
            InlineCheckboxes('state'),
        )


class BookingItemFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field_with_label.html'
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            'structure',
            InlineCheckboxes('state'),
        )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('structure', 'title', 'org_type', 'contact', 'email', 'tel', 'state', 'description')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        structures = Structure.objects.centers().for_user(user).order_by('name')
        if len(structures) == 1:
            kwargs['initial']['structure'] = structures[0]
        kwargs['initial']['state'] = BookingState.objects.get(title='Prospect')
        super().__init__(*args, **kwargs)
        self.fields['structure'].queryset = structures
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="row"><div class="col-md-6">'),
            'title',
            'structure',
            'description',
            HTML('</div><div class="col-md-6">'),
            'state',
            'org_type',
            'contact',
            'email',
            'tel',
            HTML('</div></div>'),
            Submit('create', 'Ajouter'),
        )