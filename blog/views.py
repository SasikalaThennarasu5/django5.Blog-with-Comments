from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from .models import Post, Comment
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        return self.get_object().author == self.request.user


@require_POST
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    text = request.POST.get("text")
    if text:
        Comment.objects.create(post=post, user=request.user, text=text)
    return redirect(post.get_absolute_url())


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return HttpResponseForbidden("You cannot delete this comment")
    url = comment.post.get_absolute_url()
    comment.delete()
    return redirect(url)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
