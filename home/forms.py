from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Category, Contents, Comment



class RegistrationForm(UserCreationForm):

# ------ THIS METHOD(1) ALSO WORKS -------
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields["username"].widget.attrs.update({
    #         'name': 'username',
    #         'type': 'text',
    #         'class': 'form-control',
    #         'placeholder': 'user_name',
    #     })

#  ----- WORKS ALSO THIS METHOD (2) -----------
    password1 = forms.CharField( widget=forms.PasswordInput( attrs={'class': 'input-field', 'placeholder': 'Password',} ) ,
                                 label='Enter Password',
                                )

    password2 = forms.CharField( widget=forms.PasswordInput(attrs={ 'class': 'input-field', 'placeholder': 'Confirm Password',} ) ,
                                 label='Confirm Password',
                                 
                                )

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']

#  ----- WORKS ALSO THIS METHOD (2) -----------

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'user_name',
            }),
            'email': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'example@gmail.com',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Last Name',
            }),
        }


# cat_choose = [ ('Technology' , 'Technology'), ('Sports' , 'Sports'), ('News', 'News') ]


cat_choose = Category.objects.all().values_list('name', 'name')

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Contents
        fields = ['title', 'descript',  'category', 'picture',]
        labels = {'descript': 'Description', 'picture': 'Thumbnail'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field'}),
            'descript': forms.Textarea(attrs={'class': ''}),
            'category': forms.Select( attrs={'class': 'input-field'}),
            'picture': forms.FileInput( attrs={'class': 'input-field'}),
        }




class EditedPassChangeForm(PasswordChangeForm):
    old_password = forms.CharField( label= "Current Password",
        widget=forms.PasswordInput(attrs={'id': 'current-password','class': 'form-control'}))

    new_password1 = forms.CharField(
        label='Enter New Password',
        widget=forms.PasswordInput(attrs={'id': 'new-password','class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'id': 'confirm-password','class': 'form-control'})
    )

    class Meta:
        model = User


# ---------------==========+++++++++++===========-----------

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = "__all__"
        exclude = ['content']

        # widgets = {
        #     'commenter_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'commenter_photo': forms.FileInput(attrs={'class': 'form-outline'}),
        #     'comment': forms.TextInput( attrs={'class': 'form-select'}),
        # }