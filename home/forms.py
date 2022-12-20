from django import forms 
from .models import Post, Comment, Tag, PageInfo
from client_side_image_cropping import ClientsideCroppingWidget
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['like_number'].help_text = 'Value of this field automatically added'

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'photo':ClientsideCroppingWidget(
                width=900,height=400,
                preview_width=600,
                preview_height=350,)
        }
    
    def save(self, commit=True):
        post = super().save(commit=False)
        post.set_like_number()

        if commit:
            post.save()

        return post 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['replay', 'text']
        widgets=  {
            'replay': forms.HiddenInput(attrs={'id':'replay_input',})
            ,
            'text':forms.Textarea(attrs={
                'id':'comment-text',
                'class':'form-control',
                'placeholder':"Add a comment now!",
            })
        }

    def save(self, post, user, commit=True):
        if post.comment_set.filter(user=user).count() < 5:
            comment =  super().save(commit=False)
            comment.user = user 
            comment.post = post 

            if commit:
                comment.save()
    
            return comment

        else:
            self.add_error('text', 'You can not comment more than 5')
            return None 


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['photo', 'title', 'description', 'info_h', 'info']
        widgets = {
            'photo':ClientsideCroppingWidget(width=900,height=400,preview_width='none' ,preview_height='none'),
            'title':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'description':forms.Textarea(attrs={
                'id':'area_input',
                'class':'form-control',
            }),
            'info_h':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'info':forms.Textarea(attrs={
                'id':'area_input',
                'class':'form-control',
            }),
        }

class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['info'].help_text = 'You can leave this field empty.'
        self.fields['info_h'].help_text = 'You can leave this field empty.'

    tag_create = forms.CharField(max_length=220, label='Category tags of your post', widget=forms.TextInput(attrs={'class':'form-control', }))
    tag_create.help_text = 'You can seprate category tags with "," (like:photo,style,camera,..) .'

    class Meta:
        model = Post 
        fields = ['photo', 'title', 'description', 'info_h', 'info']
        widgets = {
            'photo':ClientsideCroppingWidget(width=900,height=400,preview_width='none' ,preview_height='none'),
            'title':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'description':forms.Textarea(attrs={
                'id':'area_input',
                'class':'form-control',
            }),
            'info_h':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'info':forms.Textarea(attrs={
                'id':'area_input',
                'class':'form-control',
            }),
        }

    def clean_tag_create(self):
        tag = self.cleaned_data['tag_create']

        if tag.isnumeric():
            raise ValidationError('Numbers can not be tag!')

        return tag 


    def save(self, user, commit=True):
        post = super().save(commit=False)
        post.user = user
        

        if commit:
            post.save()

        tag = self.cleaned_data['tag_create']
        tag_list = tag.split(',')
        for i in tag_list:
            i = i.replace(' ','')

            if i:
                try :
                    tag_obj = Tag.objects.get(name__contains=i)
                except:
                    tag_obj = Tag(name=i)
                    tag_obj.save()
                
                post.tag.add(tag_obj)

        return post

class PageInfoForm(forms.ModelForm):
    class Meta:
        model = PageInfo
        fields = "__all__"
        widgets = {'photo':ClientsideCroppingWidget(width=600,height=400,preview_width=600 ,preview_height=400),}