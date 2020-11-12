from shorepass.models import Agent,Pod
from rest_framework import generics
from .serializers import AgentSerializer,PodSerializer

import urllib3
import json
from django.http import JsonResponse

# -----------Agent----------------
class AgentList(generics.ListAPIView):
	queryset = Agent.objects.filter(status=True)
	serializer_class = AgentSerializer

class AgentDetail(generics.RetrieveAPIView):
	queryset = Agent.objects.filter(status=True)
	serializer_class = AgentSerializer

# -----------POD----------------
class PodList(generics.ListAPIView):
	queryset = Pod.objects.all()
	serializer_class = PodSerializer

class PodDetail(generics.RetrieveAPIView):
	queryset = Pod.objects.all()
	serializer_class = PodSerializer

# -----------Berth---------------
# Get from Autoberth (192.168.10.20:8003) for 2 weeks onward.
def get_2weeks_berth_info(request,terminal):
	import json
	# Redis KET , LCB1_BERTH , LCMT_BERTH
	key = f'{terminal}_BERTH'
	ttl = 60*60*4 #4 hours

	# 1) check Data exist in Redis
	# 2) if yes return json
	# 3) if No , get data from Auto berth
	# 4) Save to Redis
	# 5) return json
	http = urllib3.PoolManager()
	r = http.request('GET', f'http://192.168.10.20:8003/api/voy/?f=2020-08-01&t=2020-08-06&terminal={terminal}')
	# return json.loads(r.data.decode('utf-8'))
	response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	# response = JsonResponse({'message','Hello World'}, safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response