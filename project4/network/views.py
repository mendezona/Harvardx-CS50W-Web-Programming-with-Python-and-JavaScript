from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from .models import User, Post, Like, Comment, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json


def index(request):
    return render(request, "network/index.html")

#Get profile of a user
def user(request, user, pageNumber):
    #request database for user profile
    try:
        userProfile = User.objects.get(username=user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    #order posts by timestamp
    posts = Post.objects.order_by("-timestamp").filter(user=userProfile.id)

    #pagination by 10
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(pageNumber)

    #save if object has previous 10 or next 10
    if page_obj.has_previous == True:
        hasPrevious = {"hasPrevious": True}

    else:
        hasPrevious = {"hasPrevious": False}

    if page_obj.has_next == True:
        hasNext = {"hasNext": True}

    else:
        hasNext = {"hasNext": False}

    data = [] 
    if pageNumber != None:
        data.append({"pageNumber": pageNumber})

    else:
        data.append({"pageNumber": 0})

    #add in data for JS to use
    data.append(hasPrevious)
    data.append(hasNext)
    data.append({"totalPages": page_obj.paginator.num_pages})
    data.append({"currentUsername": request.user.username})

    for post in page_obj:
        data.append(post.serialize())

    return JsonResponse(data, safe=False)


#get number of followers user has
def followers(request, user):
    #request database for user profile
    try:
        userProfile = User.objects.get(username=user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    #if requesting information on followers
    if request.method == "GET":
        following = Follow.objects.filter(user=userProfile.id, followingStatus=True).count()
        followers = Follow.objects.filter(userFollower=userProfile.id, followingStatus=True).count()

        if request.user.is_authenticated:
            #if user is viewing their own profile
            if request.user.username == userProfile.username:
                data = {
                    'following': following,
                    'followers': followers,
                    'sameUser': True,
                    'followingStatus': 'sameUser'
                }

            #if user is viewing another profile
            else:
                #check if user is being followed
                try:
                    followRequest = Follow.objects.get(user=request.user, userFollower=userProfile).followingStatus
                except Follow.DoesNotExist:
                    followRequest = False

                data = {
                    'following': following,
                    'followers': followers,
                    'sameUser': False,
                    'followingStatus': followRequest
                }

        #data for non logged in users
        else:
            data = {
                'following': following,
                'followers': followers
            }

        return JsonResponse(data, safe=False)

    #update status of follow/unfollow
    elif request.method == "PUT":
        updateStatus = json.loads(request.body)

        try:
            followRequest = Follow.objects.get(user=request.user, userFollower=userProfile)
        except Follow.DoesNotExist:
            newFollower = Follow(user=request.user, userFollower=userProfile)
            newFollower.save()
            followRequest = Follow.objects.get(user=request.user, userFollower=userProfile)
        
        followRequest.followingStatus = updateStatus["followingStatusUpdate"]
        followRequest.save()
        return JsonResponse({"message": "Follow/unfollow successful."}, status=201)


#get like counts and update like counts
def like(request, postID):
    #request database for like status
    if request.method == "GET":
        if not request.user.is_authenticated:
            try:
                post = Like.objects.filter(post=postID, likeStatus=True)
            except Like.DoesNotExist:
                return JsonResponse({"error": "Post not found."}, status=404)

            data = {"likeCount": post.count(), 
                    "userlogedIn": False,
                    "userLikeStatus": False
                    }

            return JsonResponse(data, safe=False)

        else:
            try:
                post = Like.objects.filter(post=postID, likeStatus=True)
            except Like.DoesNotExist:
                return JsonResponse({"error": "Post not found."}, status=404)

            try:
                postUserSpecific = Like.objects.get(user=request.user, post=postID)
                likeStatus = postUserSpecific.likeStatus 
            except Like.DoesNotExist:
                likeStatus = False

            data = {"likeCount": post.count(), 
                    "userlogedIn": True,
                    "userLikeStatus": likeStatus
                    }

            return JsonResponse(data, safe=False)

    #update the like count
    if request.method == "PUT" and request.user.is_authenticated:
        updateStatus = json.loads(request.body)

        try:
            post = Like.objects.get(user=request.user, post=postID)
        except Like.DoesNotExist:
            newLike = Like(user=request.user, post=Post.objects.get(id=postID))
            newLike.save()
            post = Like.objects.get(user=request.user, post=postID)

        post.likeStatus = updateStatus["likeStatusUpdate"]
        post.save()
        return JsonResponse({"message": "Like/unlike successful."}, status=201)

    else:
        JsonResponse({"error": "Unable to reach like count"}, status=404)

#All Posts view
def allPosts(request, pageNumber):
    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(pageNumber)

    if page_obj.has_previous == True:
        hasPrevious = {"hasPrevious": True}

    else:
        hasPrevious = {"hasPrevious": False}

    if page_obj.has_next == True:
        hasNext = {"hasNext": True}

    else:
        hasNext = {"hasNext": False}

    data = [] 
    if pageNumber != None:
        data.append({"pageNumber": pageNumber})

    else:
        data.append({"pageNumber": 0})

    data.append(hasPrevious)
    data.append(hasNext)
    data.append({"totalPages": page_obj.paginator.num_pages})
    data.append({"currentUsername": request.user.username})

    for post in page_obj:
        data.append(post.serialize())

    return JsonResponse(data, safe=False)


#Following view
def following(request, pageNumber):

    if request.method == "GET":
        return render(request, "network/following.html")

    elif request.method == "POST":
        # get users id's the user follows and return in flat list form
        usersFollowed = Follow.objects.filter(user=request.user, followingStatus=True).values_list('userFollower', flat=True)
        posts = Post.objects.filter(user__in=usersFollowed).order_by("-timestamp")
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(pageNumber)

        if page_obj.has_previous == True:
            hasPrevious = {"hasPrevious": True}

        else:
            hasPrevious = {"hasPrevious": False}

        if page_obj.has_next == True:
            hasNext = {"hasNext": True}

        else:
            hasNext = {"hasNext": False}

        data = [] 
        if pageNumber != None:
            data.append({"pageNumber": pageNumber})

        else:
            data.append({"pageNumber": 0})

        data.append(hasPrevious)
        data.append(hasNext)
        data.append({"totalPages": page_obj.paginator.num_pages})
        data.append({"currentUsername": request.user.username})

        for post in page_obj:
            data.append(post.serialize())

        return JsonResponse(data, safe=False)


#API view to submit post, login required to access
@login_required
def compose(request):

    #submitting new post must be via POST
    if request.method !=  "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    else:
        #get content that user posted
        data = json.loads(request.body)
        content = data.get("content")

        #save new post
        newPost = Post(user=request.user, content=content)
        newPost.save()

        return JsonResponse({"New post status": "successful"}, status=201)


#edit post
@login_required
def edit(request, postID):

    #submitting new post must be via POST
    if request.method !=  "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    else:
        #get content that user posted
        data = json.loads(request.body)
        newText = data.get("content")
        post = Post.objects.get(id=postID)

        #save new post
        post.content = newText
        post.save()

        return JsonResponse({"New post status": "successful"}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
