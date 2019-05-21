from django import forms
from .models import *

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['main_user', 'profile', 'upload_date', 'likes', 'comments']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude=['main_user','image', 'upload_date']

class Likes(forms.ModelForm):
    class Meta:
        model=Image
        exclude=['likes','comments','upload_date','main_user','profile','image_path','caption']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['main_user', 'followers', 'following']

class FollowForm(forms.ModelForm):
    class Meta:
        model=Contact
        exclude=['user_from','user_to','created']
