from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(response):
    posts = Post.objects.order_by("-published_date")[:2]  # Get the 5 most recent posts
    context = {
        "posts": posts,
    }
    # return render(request, "blog/home.html", context)
    return render (response, "blog/home.html", context)

def logout(response):   
    return render (response, "blog/logout.html", {})

def login(response):
    return render(response, "blog/login.html", {})

def posts(response):
    return render(response, "blog/posts.html", {})

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, "Registration succesful. You can proceed to log in.")
        return redirect("login")
    else:
        form = RegisterForm()
    return render(response, "blog/register.html", {'form': form})

@login_required
def profile(response):
    return render (response, "blog/profile.html", {})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    return render(request, 'blog/edit_profile.html', {'user': request.user})

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post  # Import the Post model
from django.db.models import Q

# ListView to display all blog posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # Template for listing posts
    context_object_name = "posts"
    ordering = ["-published_date"]  # Display newest posts first

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("search")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)  # Search by tags
            ).distinct()
        return queryset

# DetailView to show individual blog posts
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"  # Template for post detail

# CreateView for authenticated users to create new posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"  # Shared form template

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign logged-in user as author
        return super().form_valid(form)

# UpdateView for authors to edit their posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can edit

# DeleteView for authors to delete their posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts")  # Redirect to post list after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only author can delete
    
class PostsByTagView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs.get("tag")
        return Post.objects.filter(tags__name=tag_name)

#new line
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/add_comment.html"

    def form_valid(self, form):
    # Get the `Post` object based on the `pk` from the URL
        post_id = self.kwargs['pk']
        form.instance.post = get_object_or_404(Post, pk=post_id)  # Use `post`, not `post_id`
        form.instance.author = self.request.user  # Assign the logged-in user as the comment author
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs["post_id"]})
    

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/edit_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/delete_comment.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.id})

