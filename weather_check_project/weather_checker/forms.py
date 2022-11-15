from django import forms


class address_form(forms.Form):

    def __init__(self, * args, searched_address, alternative_addresses, **kwargs):
        super(address_form, self).__init__(*args, **kwargs)
        self.fields['address'] = forms.CharField(widget=forms.Textarea(
            attrs={'rows': 3, 'class': 'formTextInput'}))
        self.fields['address'].initial = searched_address
        self.fields['alternative_addresses'] = forms.CharField(widget=forms.Select(
            choices=alternative_addresses, attrs={'onchange': 'address_form.submit();'}), required=False)
        # self.fields['metric'] = forms.ChoiceField(choices=[('metric', 'metric'), ('imperial', 'imperial')],
        #                                           widget=forms.RadioSelect)
