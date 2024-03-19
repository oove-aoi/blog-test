from urllib.parse import unquote
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from python_ipware  import IpWare
from django.db.models import Count

from .forms import CustomUserCreationForm, PostCreationForm, PostUpdateForm, CommentCreationForm
from .models import IpAddress, Post, Comment

# Create your views here.
#首頁
def index(request):
	viewcount = get_object_or_404
	post_views_count = Post.objects.annotate(viewer_count=Count('viewersip')).order_by("-viewer_count")
	top_five_of_viewscount = post_views_count[:5]
	
	classification = Post.post_class

	return render(request, "posts/index.html",{
		"postlist_viewercount": top_five_of_viewscount,
		"classification": classification,
	})

def classlist(request):
	selected_classification_encoded = request.GET.get("classification", None)
	selected_classification = unquote(selected_classification_encoded)
	error_message = ''
	selected_classification_value = None
	classification = Post.post_class
	
	for value, label in Post.post_class:
		if label == selected_classification:
			selected_classification_value = value
			break

	else:
		error_message = "無此分類，請確認你的分類正確"

	#依照分頁數篩選出想要顯示的帖子
	class_list = Post.objects.filter(classification=selected_classification_value).order_by("-post_time")
	paginator = Paginator(class_list, 5)
	page_number = request.GET.get("page", 1)
	page_obj = paginator.get_page(page_number)

	return render(request, 'posts/classification_list_page.html', {
		"classification": classification,
		"selected_classification": selected_classification,
		"error_message": error_message,
		"page_number": page_number,
		"page_obj": page_obj
	})



#user相關
def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('index')
		print(form.errors)
	else:
		form = CustomUserCreationForm()

	return render(request, 'users/register.html', {
		'form': form
	})

def userblog(request, user_id):
	blog_owner = get_object_or_404(User, id=user_id)
	blog_post = Post.objects.filter(poster__id=user_id).order_by("-post_time")

	return render(request,'posts/user-blog.html',{
		"blog_owner": blog_owner,
		"posts": blog_post
	})

#djanog5logoutview已被棄用
'''
@login_required
def user_logout(request):
	logout(request)
	return render(request, 'registration/logged_out.html', {})
'''
#post相關

@login_required
def createpost(request):
	if request.method == 'POST':
		form = PostCreationForm(request.POST, request.FILES)
		form.instance.poster = request.user

		ipw = IpWare()
		meta = request.META
		posterip, _ = ipw.get_client_ip(meta)
		posterip_str = str(posterip)

		if IpAddress.objects.filter(ip=posterip_str).exists():
			form.instance.posterip = IpAddress.objects.get(ip=posterip_str)
		else:
			new_ip = IpAddress.objects.get_or_create(ip=posterip_str)
			form.instance.posterip = IpAddress.objects.get(ip=posterip_str)

		if form.is_valid():
			post = form.save()
			return redirect('index')
		else:
			return False, form.errors
	else:
		form = PostCreationForm()

	return render(request, 'posts/post-CreateAndUpdate.html', {
		'form': form,
		'title': "創建新帖"
	})


def postdetail(request, user_id, slug):
	select_post = get_object_or_404(Post, slug=slug)
	all_comment = Comment.objects.filter(post_id=select_post.id)

	if request.method == 'POST':
		comment_form = CommentCreationForm(request.POST)

		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = select_post
			new_comment.user = request.user
			new_comment.save()
	else:
		comment_form = CommentCreationForm()

		#獲取IP，並判斷是否已經看過這個帖子並依此來決定是否增加觀看數
		#主要參考:https://dev.to/siumhossain/unique-view-count-in-specific-objectview-django-rest-framework-27be
		ipw = IpWare()
		meta = request.META
		ip, _ = ipw.get_client_ip(meta)
		ip_str = str(ip)

		if IpAddress.objects.filter(ip=ip_str).exists():
			if select_post.posterip != ip_str:
				select_post.viewersip.add(IpAddress.objects.get(ip=ip_str))
			
		else:
			new_ip, created = IpAddress.objects.get_or_create(ip=ip_str)
			if created:
				select_post.viewersip.add(new_ip)


	return render(request,'posts/post-detail.html',{
		"post": select_post,
		"viewer_count": select_post.get_viewersip_count(),
		"comments": all_comment,
		'comment_form': comment_form,
	})

def updatepost(request, user_id, slug):
	instance = get_object_or_404(Post, slug=slug)

	if request.method == 'POST':
		form = PostUpdateForm(request.POST, request.FILES,instance=instance)
		

		if form.is_valid():
			post = form.save()
			return redirect("post-detail", user_id=user_id, slug=slug)
		else:
			return False, form.errors
	else:
		form = PostUpdateForm(instance=instance)

	return render(request, 'posts/post-CreateAndUpdate.html',{
		'form': form,
		'title': "更新舊帖"
	})

def deletepost(request, user_id, slug):
	post = get_object_or_404(Post, slug=slug)
	post.delete()

	return redirect("user-blog", user_id=user_id)
	

