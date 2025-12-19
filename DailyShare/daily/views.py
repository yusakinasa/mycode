import hashlib
from functools import wraps

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# Create your views here.
from .models import Plan,  UserProfile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import *

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            return JsonResponse({'code': 401, 'msg': '未携带token'})

        profile = UserProfile.objects.filter(token=token).first()
        if not profile:
            return JsonResponse({'code': 401, 'msg': '无效token'})

        request.user = profile.user
        request.profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped_view

class TokenRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        profile = UserProfile.objects.filter(token=token).first()
        if not profile:
            return JsonResponse({'code': 400, 'msg': '无效token'})
        else:
            request.user = profile.user
            return super(TokenRequiredMixin, self).dispatch(request, *args, **kwargs)


@api_view(['GET', 'POST'])
@token_required
def fixed_plan(request):
    if request.method == 'GET':
        plans = Plan.objects.filter(is_fixed=True,user=request.profile )
        serializer = PlanGetSerializer(plans, many=True)
        return JsonResponse({'code':100,'msg':"success",'result':serializer.data})
    if request.method == 'POST':
        serializer = PlanAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.profile)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def plan_detail(request, plan_id):
    try:
        plan = Plan.objects.get(pk=plan_id)
    except Plan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PlanGetSerializer(plan)
        return JsonResponse({'code':100,'msg':"success",'result':serializer.data})
    if request.method == 'PUT':
        serializers = PlanAddSerializer(plan, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        plan.delete()
        return JsonResponse({'code':100,'msg':"success"})

    if request.method == 'PATCH':
        serializer = PlanPartialUpdateSerializer(
            plan,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'code': 100, 'msg': 'success', 'result': serializer.data})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def record(request):
    records = Record.objects.select_related('user', 'user__user').filter(upload=True)
    serializer = RecordSerializer(records, many=True)
    return JsonResponse({'code': 100, 'msg': "success", 'result': serializer.data})



@api_view(['POST'])
@token_required
def record_add(request):
    serializers = RecordAddSerializer(data=request.data)
    if serializers.is_valid():
        record_instance = serializers.save(user=request.profile)

        # 用完整字段的 Serializer 再序列化一次
        full_serializer = RecordSerializer(record_instance)  # 这里用完整字段的 Serializer
        return JsonResponse({'code': 100, 'msg': 'success', 'result': full_serializer.data},
                            status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def record_detail(request, record_id):
    try:
        record = Record.objects.get(pk=record_id)
    except Record.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializers = RecordActivateSerializer(record, data=request.data)
    if serializers.is_valid():
        serializers.save()
        return JsonResponse(serializers.data, status=status.HTTP_200_OK)
    return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_username_by_token(request):
    # 从 header 获取 token
    token = request.META.get('HTTP_TOKEN')  # header 中 'Token: xxx' → HTTP_TOKEN
    if not token:
        return JsonResponse({'code': 400, 'msg': '缺少 token'})

    # 查找对应 UserProfile
    profile = UserProfile.objects.filter(token=token).first()
    if not profile:
        return JsonResponse({'code': 401, 'msg': '无效 token'})

    # 返回 username
    username = profile.user.username
    return JsonResponse({'code': 100, 'msg': 'success', 'username': username})




###########################   token  ###############


class UserView(TokenRequiredMixin,View):

    def get(self, request):
        users = User.objects.all()
        res_list =[]
        for user in users:
            res_list.append({
                "username": user.username,
                "phone": user.userprofile.phone,
            })
        return JsonResponse({'code':100,'msg':"success","content":res_list})





class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request):
        pay_load = json.loads(request.body)
        username = pay_load.get('username')
        password = pay_load.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            return JsonResponse({'code': 400, 'msg': "不存在该用户"})


        # ✅ 关键：确保 UserProfile 一定存在
        profile,_= UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone': '1'
            }
        )

        if not profile.token:
            profile.token = self.generate_token(username)
            profile.save()

        return JsonResponse({
            'code': 100,
            'msg': "success",
            'token': profile.token,
        })

    def generate_token(self,username):
        return hashlib.md5(username.encode('utf-8')).hexdigest()



#  创建用户接口
@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse({
            "code": 100,
            "msg": "用户创建成功",
            "result": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    return JsonResponse({
        "code": 400,
        "msg": "参数错误",
        "errors": serializer.errors
    }, status=400)




