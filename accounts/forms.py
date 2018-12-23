from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserCreateForm(UserCreationForm):

    def clean_email(self):
        data = self.cleaned_data['email']
        # logic based on emailhunter.co should be implemented here!!!
        if data == "assa@buc.com":  # dummy logic for testing purposes
            raise ValidationError("Non existing mail address!!!")
        return data

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


