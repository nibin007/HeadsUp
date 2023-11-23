from django import forms


class AddForm(forms.Form):



    note = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name this day (anything you like)',
                'class': " form-control mb-3",
            }
        ),
        label='',
        required=True
    )

    content = forms.CharField(
        widget=forms.Textarea(
            {
                'placeholder': 'Write what you feel...',
                'class': "form-control quilljs-textarea",
                'row': "15"
            }
        ),
        label='',
        required=True
    )
