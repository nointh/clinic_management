from account.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username',)
