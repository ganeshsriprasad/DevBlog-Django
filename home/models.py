from django.db import models
from django.db import models
from django.contrib.auth.models import User
from .backend import custom_slugify
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True, default='')
    descript = RichTextField(blank=True, null=True)
    uploaded_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to="blog_thumb/", null=True, default='no_thumb.png')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='contents')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.ForeignKey(Contents, on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=50)
    commenter_photo = models.ImageField(upload_to="viewer_pic/", null=True, default='avatar.png')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, default='avatar.png')
    bio_data = models.TextField(blank=True, null=True, default='')
    
    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name) 
            if value is None or value=='':
                return False
        return True
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

def save_profile(sender, instance,**kwargs):
    instance.profile.save()


class SayToMe(models.Model):
    name_is = models.CharField( max_length=180, null=True, blank=True)
    saying = models.TextField()

class MsgFromAdmin(models.Model):
    mymsg = models.CharField(max_length=500, null=True, blank=True)
    logo = models.ImageField(upload_to="Logos", default="avatar.png")
