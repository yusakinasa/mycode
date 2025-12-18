import hashlib

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
from .models import Plan, Welcome, UserProfile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import *


# def fixed_plan(request):
#     plans = Plan.objects.all().values(
#         'plan_name',
#         'start_time',
#         'end_time',
#         'state',
#         'is_fixed'
#     )
#     return JsonResponse({'code':100,'msg':"success",'result':list(plans)})


@api_view(['GET', 'POST'])
def fixed_plan(request):
    if request.method == 'GET':
        plans = Plan.objects.filter(is_fixed=True)
        serializer = PlanGetSerializer(plans, many=True)
        return JsonResponse({'code':100,'msg':"success",'result':serializer.data})
    if request.method == 'POST':
        serializer = PlanAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

@api_view(['GET','POST'])
def record(request):
    if request.method == 'GET':
        records = Record.objects.select_related('user_id').all().filter(upload=True)
        serializer = RecordSerializer(records, many=True)
        return JsonResponse({'code': 100, 'msg': "success", 'result': serializer.data})
    if request.method == 'POST':
        serializers = RecordAddSerializer(data=request.data)
        if serializers.is_valid():
            record_instance = serializers.save()

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


###########################   token  ###############
class UserView(View):

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
            return JsonResponse({'code':400,'msg':"不存在该用户"})
        else:
            # generate token
            token = self.generate_token(username)
            user.userprofile.token = token
            user.userprofile.save()
            user.save()

            return JsonResponse({'code':100,'msg':"success","token":token})

    def generate_token(self,username):
        return hashlib.md5(username.encode('utf-8')).hexdigest()

class TokenRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTH')
        user = User.objects.filter(token=token).first()
        if not user:
            return JsonResponse({'code':400,'msg':"无效token"})
        else:
            return super(TokenRequiredMixin, self).dispatch(request, *args, **kwargs)