from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from home.views import SpeciesViewSet

from home import views

router = DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    path('species_id/<int:species_id>/', views.species_id, name='species_id'),
    path('species/', views.species, name='species'),
    re_path('^', include(router.urls)),
]