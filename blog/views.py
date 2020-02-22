from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import AnotherForm,UpdateBlogPostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.http import HttpResponse
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
#from .settings import SUMMERNOTE_THEME

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #content = forms.CharField(widget=SummernoteInplaceWidget())
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        return super().form_valid(form)
        


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def edit_blog_view(request, id):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("login")

	post = get_object_or_404(Post, id=id)

	if post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			post = obj

	form = UpdateBlogPostForm(
			initial = {
					"title": post.title,
					"content": post.content,
					
			}
		)

	context['form'] = form
	return render(request, 'blog/t.html', context)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required    
def sumtest(self):
        
    #instance = Post(author=self.user)
    #form = AnotherForm(instance=instance)
    if self.method == 'POST':
        form = AnotherForm(self.POST,self.FILES)
        if form.is_valid():
            #post_author.id=self.user.id
            form.instance.author = self.user
            #post.author = request.user
            post_item = form.save(commit=False)
            post_item.save()
        return redirect('blog-home')
    else:
        form = AnotherForm()    
    return render(self, 'blog/test.html', {'form': form})


def t(request):
    return render(request, 'blog/dem.html')




