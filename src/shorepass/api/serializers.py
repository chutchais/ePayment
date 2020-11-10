from rest_framework import serializers
from shorepass.models import Agent,Pod

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('name','fullname','status')


class PodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pod
        fields = ('name','description','actual_pod','status')