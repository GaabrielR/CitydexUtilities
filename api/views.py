from rest_framework.viewsets import ModelViewSet
from .models import City
from .serializers import CitySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import IntegerField
from django.db.models.functions import Cast

class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def cities_view(request):
    colors = request.GET.getlist('colors')
    available_colors = ["Verde", "Vermelho", "Azul", "Amarelo"]

    cities = City.objects.annotate(
        description_num=Cast('description', IntegerField())
    ).order_by('description_num', 'name')

    if colors:
        for color in colors:
            cities = cities.filter(colors__icontains=color)

    return render(request, 'cities_public.html', {
        'cities': cities,
        'selected_colors': colors,
        'available_colors': available_colors
    })

def filter_cities_view(request):
    colors = request.GET.getlist('colors')

    cities = City.objects.annotate(
        description_num=Cast('description', IntegerField())
    ).order_by('description_num', 'name')

    if colors:
        # Filtra as cidades que contêm TODAS as cores selecionadas
        for color in colors:
            cities = cities.filter(colors__icontains=color)

    cities_data = [
        {
            'name': city.name,
            'description': city.description,
            'image_url': city.image.url if city.image else None,
            'colors': city.colors
        }
        for city in cities
    ]
    
    return JsonResponse({'cities': cities_data})