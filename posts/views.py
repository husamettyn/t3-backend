from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # For access control
from .models import Post

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html' # Template to be created later
    context_object_name = 'posts'

# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html' # Template to be created later
    context_object_name = 'post'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView): # Require login
    model = Post
    template_name = 'posts/post_form.html' # Template to be created later
    fields = ['title', 'content', 'image'] # Fields for the form
    success_url = reverse_lazy('post_list') # Redirect after creation

    def form_valid(self, form):
        form.instance.author = self.request.user # Set author automatically
        return super().form_valid(form)

# Update an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Require login and author check
    model = Post
    template_name = 'posts/post_form.html' # Re-use the form template
    fields = ['title', 'content', 'image'] # Fields for the form
    success_url = reverse_lazy('post_list') # Redirect after update

    def test_func(self): # Check if the current user is the author
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # Require login and author check
    model = Post
    template_name = 'posts/post_confirm_delete.html' # Template to be created later
    success_url = reverse_lazy('post_list') # Redirect after deletion

    def test_func(self): # Check if the current user is the author
        post = self.get_object()
        return self.request.user == post.author
