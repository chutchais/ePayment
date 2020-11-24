from rest_framework import serializers
from shorepass.models import Agent,Pod,Customer

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('name','fullname','status')


class PodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pod
        fields = ('name','description','actual_pod','status')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('pk','name','address','tax','branch','description','status')