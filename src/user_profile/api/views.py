from user_profile.models import Address
from rest_framework import generics
from .serializers import AddressSerializer

# # -----------Agent----------------
class AddressList(generics.ListAPIView):
	queryset = Address.objects.filter(status=True)
	serializer_class = AddressSerializer
	pagination_class = None
	
	def get_queryset(self):
		current_user = self.request.user
		return Address.objects.filter(user=current_user,status=True).order_by('company')


class AddressDetail(generics.RetrieveAPIView):
	queryset = Address.objects.filter(status=True)
	serializer_class = AddressSerializer