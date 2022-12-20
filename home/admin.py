from django.contrib import admin
from .models import Post, Tag, Comment, Link, PageInfo
from django.contrib import messages 
from client_side_image_cropping import DcsicAdminMixin
from .forms import PostForm, PageInfoForm, PostUpdateForm
from client_side_image_cropping import DcsicAdminMixin

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(DcsicAdminMixin):
    form = PostForm
    actions = ['maked_blocked']
    list_display = ['title', 'user', 'created', 'like_number']
    inlines = [CommentInline]

    @admin.action(description='Block selected posts')
    def maked_blocked(self, request, queryset):
        queryset.update(status='block')
        self.message_user(request, f'{queryset.count()} Selected posts successfully blocked', messages.SUCCESS)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'post', 'replay', 'user']


@admin.register(PageInfo)
class PageInfoAdmin(DcsicAdminMixin):
    form = PageInfoForm


admin.site.register(Link)
admin.site.register(Tag)