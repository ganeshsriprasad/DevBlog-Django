from django.contrib import admin
from .models import Contents ,Category , Comment, MsgFromAdmin, SayToMe, UserProfile
# Register your models here.

@admin.register(Contents)
class SeeContents(admin.ModelAdmin):
    list_display = ['user','title','uploaded_at','updated_at','category','likes','dislikes','views','descript','picture','slug',]
    # fields='__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Comment)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('content', 'commenter_name', 'commenter_photo', 'comment',)

admin.site.register(UserProfile)


@admin.register(SayToMe)
class UserSayToMe(admin.ModelAdmin):
    list_display = ('name_is', 'saying', )


admin.site.register(MsgFromAdmin)