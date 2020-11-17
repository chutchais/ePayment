from rest_framework import serializers
from user_profile.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk','company','address','tax','branch')
