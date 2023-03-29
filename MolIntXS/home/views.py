from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.serializers import serialize
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
import home.models as DBtables
from .models import Species, EnsemblGene, MetaKey, KeyValuePair
from home.serializers import SpeciesSerializer, InteractionSerializer, EnsemblGeneSerializer
from .serializers import LazyEncoder
import json
from json import JSONEncoder
import numpy as np

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime


# Create your views here.
def index(request):
    return HttpResponse("Welcome! You're at the MolIntXS index.")

def prediction_method(request):
    return HttpResponse("Welcome! You're at the prediction_method response page.")

    #path('', views.index, name='index'),
    #path('', views.index, name='index'),
  
@swagger_auto_schema(method='get',operation_description="Returns a species object containing all the information available for the species with the provided identifier (int).")
@api_view(['GET'])
def species_id(request, species_id):
    species_list = DBtables.Species.objects.filter(species_id=species_id)
    json_species = serialize('jsonl', species_list, cls=LazyEncoder)  

    return HttpResponse(json_species)

@swagger_auto_schema(method='get',operation_description="Returns a list of all interaction objects available.\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def interactions(request):
    interaction_list = DBtables.Interaction.objects.all()
    json_interactions = serialize('jsonl', interaction_list, cls=LazyEncoder)  

    return HttpResponse(json_interactions)



@swagger_auto_schema(method='get',operation_description="Returns a list of species objects containing all the information available for a specific Ensembl species name (also known as production name) passed as a parameter using the case non sensitive format: genus_species (ie.- 'homo sapiens')")
@api_view(['GET'])
def species_by_ensembl_name(request, species_production_name):
    species_list = DBtables.Species.objects.filter(production_name__icontains=species_production_name)
    json_species = serialize('jsonl', species_list, cls=LazyEncoder)  

    return HttpResponse(json_species)


@swagger_auto_schema(method='get',operation_description="Returns a list of species objects with all the information available for a specific species scientific name passed as a parameter using the case non sensitive format: genus species (ie.- 'homo sapiens')")
@api_view(['GET'])
def species_by_scientific_name(request, species_scientific_name):
    species_list = DBtables.Species.objects.filter(scientific_name__icontains=species_scientific_name)
    json_species = serialize('jsonl', species_list, cls=LazyEncoder)  

    return HttpResponse(json_species)


# 'method' can be used to customize a single HTTP method of a view
#@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# 'methods' can be used to apply the same modification to multiple methods
#@swagger_auto_schema(methods=['put', 'post'], request_body=UserSerializer)

@swagger_auto_schema(method='get',operation_description="Returns a list of species objects annotated with a molecular interaction.\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def species(request):
    species_list = DBtables.Species.objects.all()
    json_species = serialize('jsonl', species_list, cls=LazyEncoder) 
    
    return HttpResponse(json_species)

@swagger_auto_schema(method='get',operation_description="Returns a list of all meta_value objects available.\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def meta_values(request):
    metavalues_list = DBtables.KeyValuePair.objects.all()
    json_metavalues = serialize('jsonl', metavalues_list, cls=LazyEncoder)  

    return HttpResponse(json_metavalues)


@swagger_auto_schema(method='get',operation_description="Returns a list of all meta_key objects available.\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def meta_keys(request):
    print("meta_keys")
    metakey_list = DBtables.MetaKey.objects.all()
    json_metakeys = serialize('jsonl', metakey_list, cls=LazyEncoder)  

    return HttpResponse(json_metakeys)


@swagger_auto_schema(method='get',operation_description="Returns a list of all Ensembl gene objects annotated with a molecular interaction.\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def ensembl_gene(request):
    gene_list = DBtables.EnsemblGene.objects.all()
    json_genes = serialize('jsonl', gene_list, cls=LazyEncoder) 
    
    return HttpResponse(json_genes)



@swagger_auto_schema(method='get',operation_description="Returns a list of all external databases from which we have imported molecular interaction.")
@api_view(['GET'])
def source_dbs(request):
    source_db_list = DBtables.SourceDb.objects.all()
    fields_list = []

    for db in source_db_list:
        fields_list.append({db.label:db.external_db}) 
    return HttpResponse(fields_list)

@swagger_auto_schema(method='get',operation_description="Returns all molecular interactions (listed by Ensembl species).\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def interactions_by_prodname(request):
    
    species_genes_List = []
    ensembl_gene_query_set = DBtables.EnsemblGene.objects.select_related('species')

    species_gene_dict = {}
    for eg in ensembl_gene_query_set:
        if 'UNDETERMINED' not in eg.ensembl_stable_id:
            prod_name = eg.species.production_name
            if prod_name in species_gene_dict:
                genes_list = species_gene_dict[prod_name]
                genes_list.append(eg.ensembl_stable_id)
                species_gene_dict[prod_name] = genes_list
            else:
                species_gene_dict[prod_name] = [eg.ensembl_stable_id]
    json_species_genes = json.dumps(species_gene_dict)
    return HttpResponse(json_species_genes)

@swagger_auto_schema(method='get',operation_description="Returns a list of all the interactions available for a particular Ensembl gene (defined by its Ensembl stable identifier)")
@api_view(['GET'])
def display_by_gene(request,ens_stbl_id):
    interactions_by_queried_gene = DBtables.Interaction.objects.filter(Q(interactor_1__ensembl_gene_id__ensembl_stable_id=ens_stbl_id) | Q(interactor_2__ensembl_gene_id__ensembl_stable_id=ens_stbl_id))
    interactions_results_dict = {"interactor_1":{},"interactors_2":[]}
    interactor1_dict = {}
    interactor2_dict = {}

    interactors2_list = [] 
    
    for intrctn in interactions_by_queried_gene:
        if not interactions_results_dict["interactor_1"]:
            InteractionsByGeneList = []
            interactor1_type = intrctn.interactor_1.interactor_type
            species1_name = intrctn.interactor_1.ensembl_gene.species.scientific_name 
            identifier1 = intrctn.interactor_1.curies
            ens_stbl_id_1 = intrctn.interactor_1.ensembl_gene.ensembl_stable_id
            ensembl_gene_link_1 = get_gene_link(ens_stbl_id_1)
            identifier1_url = get_identifier_link(identifier1)

            interactor1_dict = {"type":"species","name": species1_name,"gene": {"name":ens_stbl_id_1,"url":ensembl_gene_link_1},"interactor":interactor1_type,"identifier": {"name":identifier1,"url":identifier1_url}}
            interactions_results_dict["interactor_1"] = interactor1_dict
      
        interactor2_type = intrctn.interactor_2.interactor_type
        identifier2 = intrctn.interactor_2.curies
        if 'UNDETERMINED' in identifier2:
            identifier2 = 'UNDETERMINED';
        identifier2_url = get_identifier_link(identifier2)
        source_db = intrctn.source_db.label
        source_db_link = get_source_db_link(identifier1, source_db)
        interactor2_dict = {}
        if interactor2_type == 'synthetic':
            interactor2_name = intrctn.interactor_2.name
            interactor2_dict = {"type":"other", "name": interactor2_name,"interactor": interactor2_type,"identifier":{"name":identifier2,"url":identifier2_url},"source_DB": {"name":source_db,"url":source_db_link}}
        else:
            species2_name = intrctn.interactor_2.ensembl_gene.species.scientific_name 
            ens_stbl_id_2 = intrctn.interactor_2.ensembl_gene.ensembl_stable_id 
            if 'UNDETERMINED' in ens_stbl_id_2:
                ens_stbl_id_2 = 'UNDETERMINED'
            ensembl_gene_link_2 = get_gene_link(ens_stbl_id_2)
            interactor2_dict = {"type":"species", "name": species2_name,"gene": {"name":ens_stbl_id_2,"url":ensembl_gene_link_2},"interactor":interactor2_type,"identifier":{"name":identifier2,"url":identifier2_url},"source_DB":{"name":source_db,"url":source_db_link}}
        
        metadata_list = get_metadata_list(intrctn.interaction_id,source_db_link)
        interactor2_dict["metadata"] = metadata_list
        interactors2_list.append(interactor2_dict)

    if interactor1_dict != {}:
        interactions_results_dict = {"interactor_1":interactor1_dict, "interactor_2":interactors2_list}
    else:
        interactions_results_dict = {}
    json_response = json.dumps(interactions_results_dict)
    return HttpResponse(json_response)


@swagger_auto_schema(method='get',operation_description="Returns all molecular interactors (listed by their Ensembl species name, also known as production name).\nThe 'Try it out' button might return an error if the response is too big but the endpoint will still work if tried on a browser.")
@api_view(['GET'])
def interactors_by_prodname(request):
    
    species_genes_List = []
    ensembl_gene_query_set = DBtables.EnsemblGene.objects.select_related('species')

    species_gene_dict = {}
    for eg in ensembl_gene_query_set:
        if 'UNDETERMINED' not in eg.ensembl_stable_id:
            prod_name = eg.species.production_name
            if prod_name in species_gene_dict:
                genes_list = species_gene_dict[prod_name]
                genes_list.append(eg.ensembl_stable_id)
                species_gene_dict[prod_name] = genes_list
            else:
                species_gene_dict[prod_name] = [eg.ensembl_stable_id]
    json_species_genes = json.dumps(species_gene_dict)
    return HttpResponse(json_species_genes)

@swagger_auto_schema(method='get',operation_description="Returns all molecular interactors for a specific Ensembl species name (also known as production name) passed as a parameter using the case non sensitive format: genus_species (ie.- 'homo_sapiens')")
@api_view(['GET'])
def interactors_by_specific_prodname(request, species_production_name):
    
    species_genes_List = []
    ensembl_gene_query_set = DBtables.EnsemblGene.objects.select_related('species').filter(species__production_name__icontains=species_production_name).exclude(ensembl_stable_id__icontains='UNDETERMINED')

    species_gene_dict = {}
    for eg in ensembl_gene_query_set:
        prod_name = eg.species.production_name
        if prod_name in species_gene_dict:
            genes_list = species_gene_dict[prod_name]
            genes_list.append(eg.ensembl_stable_id)
            species_gene_dict[prod_name] = genes_list
        else:
            species_gene_dict[prod_name] = [eg.ensembl_stable_id]
    json_species_genes = json.dumps(species_gene_dict)
    return HttpResponse(json_species_genes)

@swagger_auto_schema(method='get',operation_description="Returns all molecular interactors for a specific species scientific name passed as a parameter using the case non sensitive format: genus species (ie.- 'homo sapiens')")
@api_view(['GET'])
def interactors_by_specific_scientific_name(request, species_scientific_name):
    
    species_genes_List = []
    ensembl_gene_query_set = DBtables.EnsemblGene.objects.select_related('species').filter(species__scientific_name__icontains=species_scientific_name).exclude(ensembl_stable_id__icontains='UNDETERMINED')
    
    species_gene_dict = {}
    for eg in ensembl_gene_query_set:
        science_name = eg.species.scientific_name
        if science_name in species_gene_dict:
            genes_list = species_gene_dict[science_name]
            genes_list.append(eg.ensembl_stable_id)
            species_gene_dict[science_name] = genes_list
        else:
            species_gene_dict[science_name] = [eg.ensembl_stable_id]
    json_species_genes = json.dumps(species_gene_dict)
    return HttpResponse(json_species_genes)

def get_metadata_list(interaction_id, source_db_link):
    MetadataByInteraction = DBtables.KeyValuePair.objects.filter(interaction_id=interaction_id)
    metadata_list = []
    
    for mo in MetadataByInteraction:
        metadata_dict = {}
        metadata_dict['label'] = mo.meta_key.name
        metadata_dict['value'] = mo.value
        if any(mo.meta_key.name in d.values() for d in metadata_list):
            metadata_list = [
                    {
                        'value':'Several experiments exist for this interaction. Please click  <a href=' + source_db_link + " target='_blank'>here</a>" + ' for more information'
                    }
                ]
            return metadata_list
        else:
            metadata_list.append(metadata_dict)
    return metadata_list

def get_source_db_link(identifier, source_db):
    url = ''
    if source_db == "PHI-base":
        url = "http://www.phi-base.org/searchFacet.htm?queryTerm=" + clean_identifier(identifier)
    elif source_db == "PlasticDB":
        url = "https://plasticdb.org/proteins"
    elif "HPIDB" in source_db:
        url = "https://hpidb.igbb.msstate.edu/keyword.html"
    return url

def clean_identifier(raw_id):
    if ":" in raw_id:
        clean_id = raw_id.partition (":") [2]
        return clean_id
    else:
        return raw_id

def get_identifier_link(identifier):
    url_link = None
    if "UNDETERMINED" not in identifier:
        url_link = "https://identifiers.org/" + identifier
    return url_link

def get_gene_link(ensembl_gene):
    url_link = None
    if 'UNDETERMINED' not in ensembl_gene:
        url_link = "https://ensemblgenomes.org/id/" + ensembl_gene
    return url_link

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

@api_view(['GET'])
class EnsemblGeneViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 EnsemblGene
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many EnsemblGene

      serializer_class = EnsemblGeneSerializer
      queryset = DBtables.EnsemblGene.objects.all()

