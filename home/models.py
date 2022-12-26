from django.db import models
from user.models import User 
from django.template.defaultfilters import slugify
from django.urls import reverse

how = [
    ('active','active'),
    ('block','block'),
]

class Tag(models.Model):
    name = models.CharField('Name', max_length=45, unique=True)
    text = models.TextField(max_length=220, default='No description for this tag.')
    attr = models.CharField('Icon class name', max_length=30, default='bi-tag')
    attr.help_text = 'Bootstrap icon class for example(bi-person)'
    show = models.BooleanField('show in home page', default=False)
    slug = models.SlugField(null=True, blank=True)
    slug.help_text = 'Leave this tag empty.'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f'{self.name}-{self.pk}')
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-show']


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField('Post photo', upload_to='home/post_photo')
    title = models.CharField('Title', max_length=85)
    description = models.TextField("Description", max_length=420)
    info_h = models.CharField('Information header', max_length=55, null=True, blank=True)
    info = models.TextField('Information', max_length=220, null=True, blank=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True)
    status = models.CharField('Status', choices=how, max_length=10, default="active")
    created = models.DateTimeField('Created time', auto_now_add=True)
    likes = models.ManyToManyField(verbose_name='Liked by user',to=User, related_name='liked_user', related_query_name='liked_user', blank=True)
    like_number = models.IntegerField(null=True,blank=True)
    slug = models.SlugField(null=True, blank=True)
    slug.help_text = 'Leave this tag empty.'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f'{self.title}-{self.pk}')
        return super().save(*args, **kwargs)

    def set_like_number(self):
        self.like_number = self.likes.count()

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"post_slug": self.slug})
    
    class Meta:
        ordering = ['-created']
    

class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    text = models.CharField(max_length=150, verbose_name='Comment text')
    post = models.ForeignKey(Post, models.CASCADE)
    replay = models.ForeignKey('Comment',models.CASCADE,null=True,blank=True)
    
    def __str__(self) -> str:
        if self.replay:
            how='child'
        else:
            how='parent'

        return f'{how}class-{self.post}'

    def save(self, *args, **kwargs):
        if self.replay:

            if self.replay == self:
                raise ValueError('Comments can not replay itselfs')

            if self.replay.replay:
                raise ValueError('You can\'t replay a child comment')   
            
            if self.post != self.replay.post:
                raise ValueError('You can not replay a comment from another post')

        return super().save(*args, **kwargs)


class Link(models.Model):
    name = models.CharField(max_length=85)
    url = models.URLField(max_length=200)
    icon = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.url


class PageInfo(models.Model):
    photo = models.ImageField('Post photo', upload_to='home/page_info')
    text = models.TextField(max_length=225)
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)
    admin_user.help_text = 'You can leave empty this field.'

    def __str__(self) -> str:
        return self.admin_user.username
        
    class Meta:
        verbose_name= 'Page information'
    
    def save(self, *args, **kwargs):
        self.admin_user = User.objects.filter(is_admin=True)[0]
        return super().save(*args, **kwargs)