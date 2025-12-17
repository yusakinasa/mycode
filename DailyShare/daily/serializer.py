from rest_framework import serializers

from daily.models import Plan

# 获取计划
class PlanGetSerializer(serializers.ModelSerializer):
    state_text = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['plan_name', 'start_time', 'end_time','state_text']

    def get_state_text(self, obj):
        return '进行中' if obj.state else '未开始'

# 添加计划
class PlanAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'user_id',
            'plan_name',
            'start_time',
            'end_time',
            'is_fixed',
        ]

class PlanPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['state', 'start','plan_name','start_time','end_time']




