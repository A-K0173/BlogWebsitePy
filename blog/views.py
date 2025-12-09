from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Create your views here.
@login_required
def create_post(request):
	"""
    Handles Blog post creation:
    - GET: i dont know yet bruh
    - POST: Save the form and redirect
    """
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/create_post.html', {'form': form})