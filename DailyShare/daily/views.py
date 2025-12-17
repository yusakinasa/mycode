from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status

# Create your views here.
from .models import Plan, Welcome

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