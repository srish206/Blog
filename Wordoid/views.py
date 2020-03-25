from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from Wordoid.models import Post
from Wordoid.models import Comment
import json
import datetime

from Wordoid.forms import PostForm
from Wordoid.forms import CommentForm

from django.template import loader
import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
# from htmlmin.decorators import minified_response
from django.core.paginator import Paginator

# Create your views here.


# @csrf_exempt
# def home_page(request):
# 	posts = Post.objects.all()
# 	comments = []
# 	for comment in posts:
# 		comments.append(comment.post.values('post','user','text_field'))
# 	dict_data = {
# 		'post':posts,
# 		'comment':comments
# 	}
# 	if not request.user.is_authenticated:
# 		# import pdb;pdb.set_trace()
# 		return render(request,"post/home.html",dict_data)
# 	else:
# 		# import pdb;pdb.set_trace()
# 		return render(request,"post/home.html",dict_data)




@csrf_exempt
def home_page(request):
	post_data = []
	posts = Post.objects.all()

	for post in posts:
		post_data.append({
				"id": post.id,
				"title": post.title,
				"description": post.description,
				"author": post.auther,
				"is_liked": post.liked_users.filter(id=request.user.id).exists(),
				"like_count":post.user_like,
				"comments": post.post.all(),
			})

	page = request.GET.get('page', 1)
	paginator = Paginator(post_data,3)

	try:
		posts_page = paginator.page(page)
	except PageNotAnInteger:
		posts_page = paginator.page(1)
	except EmptyPage:
			posts_page = paginator.page(paginator.num_pages)

	
	dict_data = {
		'posts':posts_page
	}
	if not request.user.is_authenticated:
		return render(request,"post/home.html",dict_data)
	else:
		return render(request,"post/home.html",dict_data)
	# return HttpResponse("home")

@csrf_exempt
@login_required
def show_post(request):
	show_all_post = Post.objects.filter(auther=request.user)
	dict_post = {
		'all_post':show_all_post
	}
	return render(request,"post/show_post.html",dict_post)

@csrf_exempt
@login_required
def change_post(request,id):
	post=Post.objects.get(id=id)
	# post_publish = post.publish if False else True
	# post.publish = post_publish
	# post.save()
	# import pdb;pdb.set_trace()
	if post.publish == False:
		post.publish=True
		post.save()
		return redirect(publish_post)
	elif post.publish == True:
		post.publish=False
		post.save()
		return redirect(unpublish_post)


@csrf_exempt
def add_post(request):
	# code for adding post
	title = request.POST.get('"title')
	description = request.POST.get('description')
	today_date = datetime.datetime.now().strftime ("%Y-%m-%d")
	up_date = datetime.datetime.now().strftime ("%Y-%m-%d")
	# we have two methods to save post creat() and save()
	post_instance = Post.objects.create(title=title,description=description,publish_date=today_date,update_date=up_date)
	# post_instance = Post(title=title,description=description,publish_date=today_date,update_date=up_date)
	# post_instance.save()


@csrf_exempt
def post_model_form(request):
	if request.method == 'POST':
		''' here we pass request in a model PostForm through this we can directly 
			save in post in a requested user'''		
		post_form = PostForm(request,request.POST)
		# post_form = PostForm(request.POST)
		# post_form.save()
		if post_form.is_valid():
			instance = post_form.save(commit=False)
			instance.auther = request.user
			instance.save()
			show_post = Post.objects.all()
			dict_post = {
				'all_post':show_post
			}
			return render(request,"post/show_post.html",dict_post)
	else:
		post_form = PostForm(request)
	return render(request,"post/post_form.html",{'form':post_form})




@csrf_exempt
def publish_post(request):
	current_user = User.objects.filter(username=request.user.username)
	user_post = Post.objects.filter(auther=current_user[0],publish=True)
	page = request.GET.get('page',1)
	paginator = Paginator(user_post,2)

	try:
		user_post = paginator.page(page)
	except PageNotAnInteger:
		user_post = paginator.page(1)
	except EmptyPage:
			user_post = paginator.page(paginator.num_pages)
	
	dict_data = {
		"posts" : user_post,
	}
	return render(request,"post/publish_page.html",dict_data)




	# post_data = []
	# if request.user.username  
	# posts = Post.objects.filter(publish=True)
	# # import pdb;pdb.set_trace()
	# for post in posts:
	# 	post_data.append({
	# 		"id": post.id,
	# 		"tit": post.title,
	# 		"description": post.description,
	# 		"auther":post.auther,
	# 		"is_liked": post.liked_users.filter(id=request.user.id).exists(),
	# 		"comment":post.post.all(),
	# 		"like_count":post.user_like,
	# 		})

	# page = request.GET.get('page',1)
	# paginator = Paginator(post_data,2)

	# # posts = Post.objects.filter(publish=True).values_list("id", "title", "description", "liked_users")
	# # post_data = []
	# # for post in posts:
	# # 	import pdb;pdb.set_trace()
	# # 	post["is_liked"] = post.post.liked_users.filter(id=request.user.id).exists()


	# 	# post_liked_data.append({
	# 	# 	"post_liked": post_liked
	# 	# 	})


	# try:
	# 	post_data = paginator.page(page)
	# except PageNotAnInteger:
	# 	post_data = paginator.page(1)
	# except EmptyPage:
	# 		post_data = paginator.page(paginator.num_pages)


	# # import pdb;pdb.set_trace()
	# dict_data = {
	# 	'posts_data':post_data,
	# 	# 'posts_page':posts_page,

	# }

	# ''' wrong way to send data in a dict'''	
	# # dict_data = {
	# # 		'posts_data':posts,
	# # 	# 'posts_data':posts {'post_liked': post_liked }
	# # }

	# return render(request,"post/publish_page.html",dict_data)



# @csrf_exempt
# def publish_post(request):
# 	test = []
# 	# comment={}
# 	for posts in Post.objects.filter(publish=True):
# 		for child in posts.post.all():
# 			# import pdb;pdb.set_trace()
# 			# test.append({'post':child.post.title,'comment':child.text_field})
# 			import pdb;pdb.set_trace()
# 			test.append([child.post.title,child.text_field])
# 	# for post in posts:
# 	# 	comment=post.post.values_list('text_field')[:2]
# 	dict_data = {
# 		'comment_data':test
# 	}
# 	# import pdb;pdb.set_trace()
# 	return render(request,"post/publish_page.html",dict_data)

@csrf_exempt
def unpublish_post(request):
	unpublish_data = Post.objects.filter(publish=False)
	dict_data = {
		'unpublish_data':unpublish_data
	}
	return render(request,"post/unpublish_page.html",dict_data)

# @minified_response
def view_post(request,id):
	if request.user.is_authenticated:
		obj = Post.objects.get(id=id)
		# obj = Post.objects.select_related('text_field').get(id=id)
		#here we have to methods 
		comment = []
		# post_comment = obj.post.all()
		# for comm in post_comment:
		# 	comment.append(comm.text_field)
		comment = obj.post.values_list('text_field')
		data = Post.objects.filter(id=id).values('title','description','publish_date','update_date')
		dict_data = {
			'data':data,
			'comment':comment
		}
		return render(request,"post/view_post.html",dict_data)	
	else:
		''' redirect is a shortcut of HttpResponseRedirect and advantage of redirect is we can pass diff. type of arguments.eg=return redirect(publish_post,id=post.id) '''		
		return redirect('/accounts/signup/')
		# return HttpResponseRedirect('/accounts/signup/')

	

def edit_post(request,id):
	obj = Post.objects.get(id=id)
	if request.method == 'POST':
		obj_form = PostForm(request,request.POST,instance=obj)
		if obj_form.is_valid():
			obj_form.save()
			return redirect(publish_post)
	
	else:
		obj_form = PostForm(request,instance=obj)
	return render(request,"post/edit_post.html",{'form':obj_form,'obj':obj})


def delete_post(request,id):
	obj = Post.objects.get(id=id)
	obj.delete()
	return redirect(publish_post)


def comment_post(request,id):
	post = Post.objects.get(id=id)
	if request.method == 'POST':
		comment = CommentForm(request.POST)
		if comment.is_valid():
			instance = comment.save(commit=False)
			instance.post = post
			instance.user = request.user
			instance.save()
			return redirect(publish_post)
	else:
		obj_form = CommentForm()
	return render(request,"post/comment_post.html",{'form':obj_form,'obj':post})





# @csrf_exempt
# def like_post(request,id):
# 	import pdb;pdb.set_trace()
# 	post = Post.objects.get(id=id)
# 	# post_like=Post.objects.filter(user=request.user,title=post)
# 	liked_user = PostLike.objects.filter(user=request.user,post=post).exists()
# 	if not liked_user:
# 		PostLike.objects.create(user=request.user,post=post)
# 	else:
# 		post_user=PostLike.objects.filter(user=request.user,post=post)
# 		find_like = post_user[0].post.like
# 		if find_like == 0:
# 			find_like += 1
# 			post.user.add(find_like)
# 			# post.save()
# 		elif find_like == 1:
# 			find_like = 0
# 			post.user.add(find_like)
# 			# post.save()
# 	return redirect(publish_post)

@csrf_exempt
def like_post(request,id):
	# import pdb;pdb.set_trace()
	like_user = False 
	post = Post.objects.get(id=id)
	''' if post.liked_users.filter(id=request.user.id).exists() == False and
	 == ' ' do not use False to check conditions '''
	if not post.liked_users.filter(id=request.user.id).exists() :
		post.liked_users.add(request.user)
		like_user = True
	else:
		post.liked_users.remove(request.user)
	# dict_data = {
	# 	# 'post': model_to_dict((post),fields=('title','liked_users')),
	# 	# 'post': model_to_dict(post),
	# 	'post_id': post.id
	# }
	# return HttpResponse(json.dumps(dict_data),li, content_type='application/json')
	dict_data = {
		'post_id': post.id,
		'like_value': like_user
	}
	# import pdb;pdb.set_trace()
	return JsonResponse({'result':dict_data})
	# return HttpResponse(json.dumps(dict_data),"post/publish_page.html",content_type='application/json')


	
# @csrf_exempt
# def like_post(request,id):
# 	# import pdb;pdb.set_trace()
# 	post = Post.objects.get(id=id)
# 	# is_liked = post.liked_users
# 	# current_user_like = Post.objects.filter(liked_users=request.user,id=id).exists()
# 	''' if post.liked_users.filter(id=request.user.id).exists() == False and
# 	 == ' ' do not use False to check conditions '''
# 	if not post.liked_users.filter(id=request.user.id).exists() :
# 		post.liked_users.add(request.user)
# 	dict_data = {
# 		'post': model_to_dict((post),fields=('title','liked_users')),
# 		'post_id': post.id
# 	}
# 	return HttpResponse(json.dumps(dict_data), content_type='application/json')

# @csrf_exempt
# def like_post(request,id):
# 	import pdb;pdb.set_trace()
# 	post_list = []
# 	post = Post.objects.get(id=id)
# 	current_user = PostLike.objects.filter(user=request.user,post=post).exists()
# 	like_obj = PostLike.objects.all()
# 	if current_user == False:
# 		PostLike.objects.create(user=request.user,post=post)
# 		return HttpResponse("like")
# 	for i in like_obj:
# 		post_list.append(i.post)
# 	if post in post_list:
# 		if post.like == 0:
# 			post.like += 1
# 			post.save()
# 		# else:
# 		elif post.like == 1:
# 			post.like = 0
# 			post.save()

# 	dict_data = {
# 		'post': model_to_dict((post),fields=('title','like')),
# 		'post_id': post.id
# 	}
# 	return HttpResponse(json.dumps(dict_data), content_type='application/json')

	''' another way to json '''
	# post_results = Post.objects.filter(id=id).values('title','like')
	# return JsonResponse({'results':list(post_results)})
	''' data get response in text formate but it is difficult to fetch the data value
		in this formate''' 	
	# return HttpResponse(json.dumps(dict_data), content_type="text/plain")
	

	# Error-it gives error bcoz post is objects of Post(queryset)
	# return JsonResponse({'results':list(post)})




def delete_comment(request,id):
	comment = Comment.objects.get(id=id)
	comment.delete()
	dict_data = {
		'comment': model_to_dict(comment),
	}
	# import pdb;pdb.set_trace()
	return JsonResponse({'results':dict_data,'result':id})
	# return HttpResponse(json.dumps(comment), content_type='application/json')
	# return redirect(publish_post)
	


def search_data(request):
	text_data=request.GET.get('text_data')
	related_post = Post.objects.filter(auther=request.user,title__icontains=text_data)
	dict_data = {
		# 'related_post':list(related_post)
		'related_post':list(related_post.values())
	}
	# import pdb;pdb.set_trace()
	return JsonResponse(dict_data)
	# return HttpResponse(dict_data,"post/publish_page.html",safe=False,content_type='application/json')