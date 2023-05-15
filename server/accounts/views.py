import json
from django.http import JsonResponse

# Create your views here.
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from share_place.models import Post
from django.core.exceptions import ObjectDoesNotExist


@require_POST
def register_user(request):
    request_body = json.loads(request.body)
    email = request_body.get('email')
    first_name = request_body.get('first_name')
    last_name = request_body.get('last_name')
    password = request_body.get('password')
    phone_number = request_body.get('phone_number')
    username = request_body.get('username')

    if User.objects.filter(email=email).exists():
        return JsonResponse(data={"message": "Email already exists"}, status=400)  # bad request

    if User.objects.filter(username=username).exists():
        return JsonResponse(data={"message": "Username already exists"}, status=400)  # bad request

    try:
        created_user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
        created_user.profile.phone_number = phone_number
        created_user.save()
        login(request, user=created_user)
    except Exception as e:
        return JsonResponse(data={"success": "Something wrong"}, status=500)

    return JsonResponse(data={"success": True})


@require_POST
def login_user(request):
    request_body = json.loads(request.body)
    username = request_body.get('username')
    password = request_body.get('password')
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse(data={'success': True})
    else:
        return JsonResponse(data={'message': "Invalid username or password"}, status=401)


@login_required
def logout_user(request):
    logout(request)
    return redirect('home_page')


@login_required
def get_users(request):
    if request.user.is_superuser or request.user:
        user_list = list(User.objects.exclude(is_superuser=True)
                                     .values('id', 'email', 'username', 'first_name', 'last_name', 'profile__phone_number','last_login'))

        for user in user_list:
            user['amount_posts'] = Post.objects.filter(author_id=user['id']).count()

        return JsonResponse(
            data={
                "users": user_list
            }
        )
    else:
        return JsonResponse(
            data={
                "message": "unauthorized"
            },
            status=401
        )


@require_http_methods(['DELETE'])
@login_required
def delete_user(request):
    if request.user.is_superuser:
        user_id = request.GET['user_id']
        try:
            user = User.objects.exclude(is_superuser=True).get(id=user_id)
            user.delete()
            return JsonResponse(
                data={
                    "success": True
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                data={
                    "message": "User not found"
                },
                status=404
            )
    else:
        return JsonResponse(
            data={
                "message": "unauthorized"
            },
            status=401
        )

