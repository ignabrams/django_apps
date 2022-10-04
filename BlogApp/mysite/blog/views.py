from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.db.models import Count
# Create your views here.

#class PostListView(ListView):
	#queryset = Post.published.all()
	#context_objects_name = 'posts'
	#paginate_by = 3
	#template_name = 'blog/post/list.html'

def post_share(request, post_id):
# Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')

	if request.method == 'POST':
	# Form was submitted
		form = EmailPostForm(request.POST)
	if form.is_valid():
			# Form fields passed validation
		cd = form.cleaned_data
		post_url = request.build_absolute_uri(post.get_absolute_url())
		subject = f"{cd[name]} recommends you read {post.title}"
		message = f"Read {post.title} at {post_url}\n\n" \
					  f"{cd['name']}\'s comments: {cd['comments']}"
		send_mail(subject, message, 'admin@myblog.com', {cd['to']})
		sent = True
	else:
		form = EmailPostForm()

	return render(request, 'blog/post/share.html', {'post': post, 'form': form})	

def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3) # 3post in each page
	page = request.GET.get('page')
	tag = PageNotAnInteger

	if tag_slug:
			tag =get_object_or404(Tag, slug=tag_slug)
			object_list = object_list.filter(tags__in=[tag])
		#paginator = Paginator(object_list, 3) # 3 posts in each page


	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, return the first page
		posts = paginator.page(1)
	except EmptyPage:
		 # If page is out of range, return the last page
		 posts = paginator.page(paginator.num_pages)

	return render(request,'blog/post/list.html', {'page': page, 'posts': posts,'tag': tag}
				)

def post_detail(request, year, month, day, slug_post):
	
	post =get_object_or_404(Post, slug=slug_post, status='published', publish__year=year, publish__month=month, publish__day=day)
	
	comments = post.comments.filter(active=True) #List fo active comments for this post
	
	new_comment = None

	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)# Create Comment object but dont save to DB yet
			new_comment.post = post     			     # Assigne the current post to the comment 
			new_comment.save()  						 # Save the comment to the database

	else:
		comment_form = CommentForm()
	return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment-form})