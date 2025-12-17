from rest_framework import serializers

from daily.models import Plan, Record


# 获取计划
class PlanGetSerializer(serializers.ModelSerializer):
    state_text = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['plan_name', 'start_time', 'end_time','state_text','state']

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
        fields = ['state','plan_name','start_time','end_time']


###################################  Record  ########################

class RecordSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()  # 如果你用 @property 计算 duration
    user_name = serializers.CharField(source='user_id.usr_name', read_only=True)

    class Meta:
        model = Record
        fields = ['user_name','end','plan_name','duration','record_id']  # ⚠️ 必须加
        # 如果不想序列化 duration，可以用 fields = ['record_id', 'user_id', 'plan_name', 'start', 'end']

    def get_duration(self, obj):
        total_seconds = int(obj.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



class RecordAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['user_id', 'start', 'plan_name']

class RecordActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['end', 'upload']

