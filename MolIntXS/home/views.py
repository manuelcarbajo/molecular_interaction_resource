from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

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
    species_list = DBtables.Species.objects.all()
    json_species = serialize('jsonl', species_list, cls=LazyEncoder) 
    
    return HttpResponse(json_species)


def prodname_ensgene(request, ens_gene, prod_name):
    #get list of interactions havig interactor1 or interactor2 corresponding to the given ens_gene and prod_name
    interactors_list = DBtables.Interaction.objects.filter(Q(interactor_1__ensembl_gene_id__ensembl_stable_id__contains=ens_gene) | Q(interactor_2__ensembl_gene_id__ensembl_stable_id__contains=ens_gene)).filter(Q(interactor_1__ensembl_gene_id__species_id__production_name__contains=prod_name) | Q(interactor_2__ensembl_gene_id__species_id__production_name__contains=prod_name))
    curated_interactor_list = DBtables.CuratedInteractor.objects.filter(curated_interactor_id__in=interactors_list)
    json_curated_interactors = serialize('jsonl', curated_interactor_list, cls=LazyEncoder) 
    return HttpResponse(json_curated_interactors)


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

