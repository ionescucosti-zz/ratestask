from .models import Prices, Ports, Regions
from rates_app.serializers import PricesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Q


class index(APIView):

    def get(self, request):
        try:
            prices = Prices.objects.all().values('orig_code', 'dest_code', 'day', 'price')[:3]
            return Response(prices)
        except Prices.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PricesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class averagePricesList(APIView):

    def get(self, request):
        try:
            date_from = request.query_params['date_from']
            date_to = request.query_params['date_to']
            origin = request.query_params['origin']
            destination = request.query_params['destination']

            orig_ports = Ports.objects.values('code').filter(parent_slug__in=Regions.objects.values('slug')
                                                             .filter(parent_slug=origin))

            dest_ports = Ports.objects.values('code').filter(parent_slug__in=Regions.objects.values('slug')
                                                             .filter(parent_slug=destination))
            orig_list = [value['code'] for value in orig_ports]
            orig_list.append(origin)
            dest_list = [value['code'] for value in dest_ports]
            dest_list.append(destination)

            prices = Prices.objects.filter(day__range=[date_from, date_to], orig_code__in=orig_list,
                                           dest_code__in=dest_list) \
                .values('day').annotate(average_price=Avg('price')).order_by('day')
            return Response(prices)
        except Prices.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class nullDaysList(APIView):

    def get(self, request):
        try:
            date_from = request.query_params['date_from']
            date_to = request.query_params['date_to']
            origin = request.query_params['origin']
            destination = request.query_params['destination']

            orig_ports = Ports.objects.values('code').filter(parent_slug__in=Regions.objects.values('slug')
                                                             .filter(parent_slug=origin))
            orig_list = [value['code'] for value in orig_ports]
            orig_list.append(origin)

            dest_ports = Ports.objects.values('code').filter(parent_slug__in=Regions.objects.values('slug')
                                                             .filter(parent_slug=destination))

            dest_list = [value['code'] for value in dest_ports]
            dest_list.append(destination)

            prices = Prices.objects.filter(day__range=[date_from, date_to], orig_code__in=orig_list,
                                           dest_code__in=dest_list) \
                .values('day').annotate(average_price=Avg('price'), prices_counter=Count('price')).order_by('day')

            for i in prices:
                if i['prices_counter'] < 3:
                    i['average_price'] = None
            return Response(prices)
        except Prices.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
