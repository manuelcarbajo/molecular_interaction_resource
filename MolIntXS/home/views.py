from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
import home.models as DBtables
from .models import Species
from home.serializers import SpeciesSerializer
from django.core.serializers import serialize
from .serializers import LazyEncoder

# Create your views here.
def index(request):
    return HttpResponse("Welcome! You're at the MolIntXS index.")

def prediction_method(request):
    return HttpResponse("Welcome! You're at the prediction_method response page.")

def species_id(request, species_id):
    species_list = DBtables.Species.objects.filter(species_id=species_id)
    json_species = serialize('jsonl', species_list, cls=LazyEncoder)  

    return HttpResponse(json_species)

def species(request):
    species_list = ()
    species_item = ''
    msg = ""

    species_list = DBtables.Species.objects.all()
    json_species = serialize('jsonl', species_list, cls=LazyEncoder) 
    
    return HttpResponse(json_species)

def ensembl_gene(request):
    return HttpResponse("Welcome! You're at the ensembl_gene response page.")

def source_db(request):
    return HttpResponse("Welcome! You're at the source_db response page.")

def meta_key(request):
    return HttpResponse("Welcome! You're at the meta_key response page.")

def ontology(request):
    return HttpResponse("Welcome! You're at the ontology response page.")

def ontology_term(request):
    return HttpResponse("Welcome! You're at the ontology_term response page.")

def curated_interactor(request):
    return HttpResponse("Welcome! You're at the curated_interactor response page.")

def predicted_interactor(request):
    return HttpResponse("Welcome! You're at the predicted_interactor response page.")

def interaction(request):
    return HttpResponse("Welcome! You're at the interaction response page.")

def key_value_pair(request):
    return HttpResponse("Welcome! You're at the key_value_pair response page.")

class SpeciesViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Species
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many Species

      serializer_class = SpeciesSerializer
      queryset = DBtables.Species.objects.all()

