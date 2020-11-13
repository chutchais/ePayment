from shorepass.models import Agent,Pod
from rest_framework import generics
from .serializers import AgentSerializer,PodSerializer

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