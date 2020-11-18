from shorepass.models import Agent,Pod,Customer
from rest_framework import generics
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .serializers import AgentSerializer,PodSerializer,CustomerSerializer

# -----------Agent----------------
class AgentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Agent
        fields = ['name']

class AgentList(generics.ListAPIView):
	queryset = Agent.objects.filter(status=True)
	serializer_class = AgentSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_class = AgentFilter

class AgentDetail(generics.RetrieveAPIView):
	queryset = Agent.objects.filter(status=True)
	serializer_class = AgentSerializer

# -----------POD----------------
class PodFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Pod
        fields = ['name']

class PodList(generics.ListAPIView):
	queryset = Pod.objects.all()
	serializer_class = PodSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_class = PodFilter

class PodDetail(generics.RetrieveAPIView):
	queryset = Pod.objects.all()
	serializer_class = PodSerializer

# -----------Customer----------------
class CustomerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['name']

class CustomerList(generics.ListAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_class = CustomerFilter
	# filterset_fields = ['name', 'tax']
	# search_fields = ['name', 'tax']

class CustomerDetail(generics.RetrieveAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer


# 
from django.http import JsonResponse
import redis
import json
db = redis.StrictRedis('redis', 6379,db=0, charset="utf-8", decode_responses=True) #Production

def get_voy_terminal(request,terminal):
	key 		= f'{terminal}_VOY_JSON'
	payload		=	db.get(key)# .decode('utf-8')
	response 	= JsonResponse(json.loads(payload), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response

def get_vessel_name_by_code(request,vessel_code):
	vessel_code 	= vessel_code.upper()
	key 			= f'VESSEL:CODE:{vessel_code}'
	vessel_name		=	db.get(key)# .decode('utf-8')
	payload 		= {
						'code':vessel_code,
						'name':vessel_name
					}
	response 	= JsonResponse(payload, safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response

def get_voy_by_vesselcode_voy(request,vessel_code,voy):
	vessel_code 	= vessel_code.upper()
	voy				= voy.upper()
	key 			= f'VESSEL:{vessel_code}:{voy}'
	voy_str			= db.get(key)# .decode('utf-8')
	response 	= JsonResponse(json.loads(voy_str), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response