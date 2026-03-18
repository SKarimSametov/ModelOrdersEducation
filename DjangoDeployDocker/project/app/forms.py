# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User, Chat, Message, Profile
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#
#
# class ChatCreateForm(forms.ModelForm):
#     participant = forms.ModelChoiceField(
#         queryset=User.objects.all(),
#         label="User 2"
#     )
#
#     class Meta:
#         model = Chat
#         fields = []
#
#
# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ["content", "file"]
#         widgets = {
#             "content": forms.TextInput(attrs={"placeholder": "введите сообщение . . ."})
#         }
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["display_name", "avatar", "bio", "age"]
#         widgets = {
#             "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Write something about yourself"}),
#         }