from django.shortcuts import get_object_or_404, render, HttpResponseRedirect 
from django.urls import reverse 
from django.views.generic import TemplateView , ListView, DetailView, UpdateView
from .models import Post, Tag, Comment, PageInfo
from django.http import JsonResponse, Http404
from .forms import CommentForm, PostUpdateForm, PostCreateForm
from django.contrib import messages

class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        # high_post top three posts with highest like_number
        context = super().get_context_data(**kwargs)
        context['high_post'] = Post.objects.order_by('-like_number')[:3]
        context['tags'] = Tag.objects.filter(show=True)[:4]
        context['page_info'] = PageInfo.objects.last()
        return context 



class PostListView(ListView):
    model = Post
    paginate_by = 9
    list_name = 'Post'

    def get_context_data(self, **kwargs):
        # list_name context variable used in template
        context =  super().get_context_data(**kwargs)
        context['list_name'] = self.list_name
        return context

    def get_queryset(self):
        # if user searched smth from GET parametr queryset are changed 

        search = self.request.GET.get('search')
        if search:
            return Post.objects.filter(title__contains=search)

        return super().get_queryset()



class PopularPostView(PostListView):
    # this view like PostListView but order of queryset comes from like_number
    list_name = 'Popular post'

    def get_queryset(self):
        # if user searched smth from GET parametr queryset are changed 
        search = self.request.GET.get('search')
        if search:
            return Post.objects.filter(title__contains=search)

        return Post.objects.order_by('-like_number')


class TagListView(PostListView):
    model = Tag 
    paginate_by = 9
    list_name = 'Tag'

    def get_queryset(self):
        # if user searched smth from GET parametr queryset are changed 
        search = self.request.GET.get('search')
        
        if search:
            return Tag.objects.filter(name__contains=search)

        return super().get_queryset()


class TagDetailView(ListView):
    template_name = 'home/tag_detail.html'
    paginate_by = 9

    def get_queryset(self):
        # if user searched smth from GET parametr queryset are changed 
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])

        search = self.request.GET.get('search')
        if search:
            return self.tag.post_set.filter(title__contains=search)

        return self.tag.post_set.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


def post_detail_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    if request.method == 'GET':
        return render(request, 'home/post_detail.html', {'post':post, 'comment_form':CommentForm()})

    # when user is commenting 
    elif request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(post, request.user)

            if comment:
                # this GET parametr for scroll window into comment form
                return HttpResponseRedirect(post.get_absolute_url()+'?commented=1')

        return render(request, 'home/post_detail.html', {'post':post, 'comment_form':form, 'commented':1})


def post_like(request, post_slug):
    do = '' 
    if request.user.is_authenticated :
        if request.method =='GET':

            post = get_object_or_404(Post, slug=post_slug)
            if not request.user in post.likes.all():
                post.likes.add(request.user)
                post.save()
                post.set_like_number()
                do = 'like'
            else:
                post.likes.remove(request.user)
                do = 'unlike'

            post.set_like_number()
            post.save()
            return JsonResponse({'do':do,'likes':post.likes.count()})
    else:
        do = None
        return JsonResponse({'do':do,'alert':'You can\'t like posts. authenticate first!'})
        

def post_delete_view(request, post_slug):

    if request.method == 'GET':
        post = get_object_or_404(Post, slug=post_slug)

        if request.user == post.user:
            return render(request, 'home/post_delete.html', {'post':post})
        else:
            raise ValueError('You can not delete this post.')

    else:
        post = get_object_or_404(Post, slug=post_slug)

        if request.user == post.user:
            messages.add_message(request, messages.ERROR, f'The post with title "{post.title}" deleted successfully.', 'danger')
            post.delete()
            return HttpResponseRedirect(reverse('user-profile',args=[post.user]))
        else:
            raise ValueError('You can not delete this post.')


class PostUpdateView(UpdateView):
    model = Post
    slug_url_kwarg = 'post_slug'
    form_class = PostUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Post Update'
        return context
    
    def get(self, request, *args, **kwargs):
        target_user = self.get_object().user
        if target_user == request.user:
            return super().get(request, *args, **kwargs)
        
        raise Http404()

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        target_user = post.user
        if target_user == request.user:
            messages.add_message(request, messages.SUCCESS, f'The post with title "{post.title}" updated successfully.')
            return super().post(request, *args, **kwargs)
        
        raise Http404()


def comment_delete(request, comment_pk):
    comment = Comment.objects.filter(pk=comment_pk)[0]
    if request.user.is_authenticated:
        if comment:
            if comment.user == request.user :
                comment.delete()
                return JsonResponse({'delete':True})

    return JsonResponse({'delete':False})


def post_create_view(request):
    user = request.user 
    if user.is_authenticated:

        if request.method == 'GET':
            return render(request, 'home/post_form.html', {'form_name':'Create new post', 'form':PostCreateForm()})

        elif request.method == 'POST':
            form = PostCreateForm(request.POST)

            if form.is_valid():
                post = form.save(user)
                messages.add_message(request, messages.SUCCESS, f'The post with title "{post.title}" created successfully.')
                return HttpResponseRedirect(post.get_absolute_url())
            else:
                return render(request, 'home/post_form.html', {'form_name':'Create new post', 'form':form})
    else:
        raise Http404()