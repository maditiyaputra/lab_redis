from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', None)
        if institution_name:
            queryset = queryset.filter(
                Q(top_sellers__contains=[{'name': institution_name}]) | Q(top_buyers__contains=[{'name': institution_name}])
                )
        return queryset
    
    def list(self, request):
        param = self.request.query_params.get('name', None)
        cache_key = f"institution: {param}"
        result = cache.get(cache_key)  
    
        if not result:  
            print('Hitting DB')  
            result = self.get_queryset() 
            
            cache.set(cache_key, result, 60)
        else:
            print('Cache retrieved!')
        
        result = self.serializer_class(result, many=True)

        return Response(result.data) 

class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sector_name = self.request.query_params.get('sector', None)
        if sector_name:
            queryset = queryset.filter(sector__icontains=sector_name)

        return queryset
    
    def list(self, request):
        param = self.request.query_params.get('sector', None)
        cache_key = f"metadata: {param}"
        result = cache.get(cache_key)
    
        if not result:  
            print('Hitting DB')  
            result = self.get_queryset() 
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache retrieved!')  
        
        result = self.serializer_class(result, many=True)

        return Response(result.data) 

class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sub_sector_name = self.request.query_params.get('sub-sector', None)

        if sub_sector_name:
            queryset = queryset.filter(sub_sector__icontains=sub_sector_name)

        return queryset
    
    def list(self, request):
        param = self.request.query_params.get('sub-sector', None)
        cache_key = f"reports: {param}"
        result = cache.get(cache_key)  
    
        if not result:
            print('Hitting DB')  
            result = self.get_queryset() 
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache retrieved!')  
        
        result = self.serializer_class(result, many=True)

        return Response(result.data) 

