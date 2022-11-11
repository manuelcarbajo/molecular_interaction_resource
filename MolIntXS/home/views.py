from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
import home.models as DBtables
from .models import Species, EnsemblGene
from home.serializers import SpeciesSerializer, InteractionSerializer, EnsemblGeneSerializer
from django.core.serializers import serialize
from .serializers import LazyEncoder
import json
from json import JSONEncoder
import numpy as np

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

def ensembl_gene(request):
    gene_list = DBtables.EnsemblGene.objects.all()
    json_genes = serialize('jsonl', gene_list, cls=LazyEncoder) 
    
    return HttpResponse(json_genes)

def interactions_by_prodname(request):
    species = DBtables.Species.objects.all()
    species_genes_List = []
    species_dict = {}
    for sp in species:
        sp_id = sp.species_id
        genes = DBtables.EnsemblGene.objects.filter(Q(curatedinteractor__interaction_for_int2__interactor_2__ensembl_gene__species_id=sp_id) | Q(curatedinteractor__interaction_for_int1__interactor_1__ensembl_gene__species_id=sp_id))
        genes_per_specie_List = []
        for gene in genes:
            if 'UNDETERMINED' not in gene.ensembl_stable_id:
                genes_per_specie_List.append(gene.ensembl_stable_id)
        if genes_per_specie_List:
            unique_gene_list = list(set(genes_per_specie_List))
            species_dict = {sp.production_name:unique_gene_list}
            species_genes_List.append(species_dict)
    json_species_genes_list = json.loads(str(species_genes_List).replace("'",'"'))
    return HttpResponse(json_species_genes_list)
        
def display_by_gene(request,ens_stbl_id):
    interactions_by_queried_gene = DBtables.Interaction.objects.filter(Q(interactor_1__ensembl_gene_id__ensembl_stable_id__contains=ens_stbl_id) | Q(interactor_2__ensembl_gene_id__ensembl_stable_id__contains=ens_stbl_id))
    interactions_results_dict = {"interactor_1":{},"interactors_2":[]}
    interactors2_list = [] 

    for intrctn in interactions_by_queried_gene:
        if not interactions_results_dict["interactor_1"]:
            InteractionsByGeneList = []
            interactor1_type = intrctn.interactor_1.interactor_type
            species1_name = intrctn.interactor_1.ensembl_gene.species.production_name 
            identifier1 = intrctn.interactor_1.curies
            ens_stbl_id_1 = intrctn.interactor_1.ensembl_gene.ensembl_stable_id
            identifier1_url = get_identifier_link(identifier1)

            interactor1_dict = {"type":"species","name": species1_name,"gene": ens_stbl_id_1,"interactor":interactor1_type,"identifier": {"name":identifier1,"url":identifier1_url}}
            interactions_results_dict["interactor_1"] = interactor1_dict
      
        interactor2_type = intrctn.interactor_2.interactor_type
        identifier2 = intrctn.interactor_2.curies
        identifier2_url = get_identifier_link(identifier2)
        source_db = intrctn.source_db.label
        source_db_link = get_source_db_link(identifier1, source_db)
        interactor2_dict = {}

        if interactor2_type == 'synthetic':
            interactor2_name = intrctn.interactor_2.name
            interactor2_dict = {"type":"other", "name": interactor2_name,"interactor": interactor2_type,"identifier":{"name":identifier2,"url":identifier2_url},"source_DB": {"name":source_db,"url":source_db_link}}
        else:
            species2_name = intrctn.interactor_2.ensembl_gene.species.production_name 
            ens_stbl_id_2 = intrctn.interactor_2.ensembl_gene.ensembl_stable_id
            interactor2_dict = {"type":"species", "name": species2_name,"gene": ens_stbl_id_2,"interactor":interactor2_type,"identifier":{"name":identifier2,"url":identifier2_url},"source_DB":{"name":source_db,"url":source_db_link}}
        
        MetadataByInteraction = DBtables.KeyValuePair.objects.filter(interaction_id=intrctn.interaction_id)
        metadata_list = []
        
        for mo in MetadataByInteraction:
            metadata_dict = {}
            metadata_dict["label"] = mo.meta_key.name
            metadata_dict["value"] = mo.value
            metadata_list.append(metadata_dict)

        interactor2_dict["metadata"] = metadata_list
        interactors2_list.append(interactor2_dict)
        
    interactions_results_dict = {"interactor_1":interactor1_dict, "interactors_2":interactors2_list}
    json_response = json.dumps(interactions_results_dict)
    return HttpResponse(json_response)


def get_source_db_link(identifier, source_db):
    url = ''
    if source_db == "PHI-base":
        url = "http://www.phi-base.org/searchFacet.htm?queryTerm=" + identifier
    elif source_db == "PlasticDB":
        url = "https://plasticdb.org/proteins"
    elif source_db == "HPIDB":
        url = "https://hpidb.igbb.msstate.edu/keyword.html"
    return url

def get_identifier_link(identifier):
    url_link = None
    if "UNDETERMINED" not in identifier:
        url_link = "https://identifiers.org/" + identifier
    return url_link

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

class EnsemblGeneViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 EnsemblGene
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many EnsemblGene

      serializer_class = EnsemblGeneSerializer
      queryset = DBtables.EnsemblGene.objects.all()

