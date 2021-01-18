from rest_framework import serializers
from rates_app.models import Ports, Prices, Regions


class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = '__all__'


class PortsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ports
        fields = '__all__'


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'

