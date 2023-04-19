from rest_framework import serializers
from django.core.serializers.json import DjangoJSONEncoder
import home.models as DBtables 


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, DBtables.Species):
            return str(obj)
        if isinstance(obj, DBtables.EnsemblGene):
            return str(obj)
        return super().default(obj)

class CuratedInteractorSerializer(serializers.Serializer):
    curated_interactor_id = serializers.IntegerField()
    prod_name = serializers.CharField(allow_null=True,source='ensembl_gene.species.production_name')
    division = serializers.CharField(allow_null=True,source='ensembl_gene.species.ensembl_division')
    ens_gene = serializers.CharField(allow_null=True,source='ensembl_gene.ensembl_stable_id')
    curies =serializers.CharField(read_only=True)
    interactor_type = serializers.CharField()

    class Meta:
        model = DBtables.CuratedInteractor

class InteractionSerializer(serializers.Serializer):
    interaction_id = serializers.IntegerField()
    interactor_1 = serializers.CharField(source='interactor_1.curies')
    interactor_2 = serializers.CharField(source='interactor_2.curies')
    doi = serializers.CharField(style={'base_template': 'textarea.html'})
    source_db = serializers.CharField(source='source_db.label')
    
    class Meta:
        model = DBtables.Interaction

class SpeciesSerializer(serializers.Serializer):
    species_id = serializers.IntegerField()
    ensembl_division = serializers.CharField(required=True, allow_blank=False, max_length=255)
    production_name = serializers.CharField(style={'base_template': 'textarea.html'})
    scientific_name = serializers.CharField(style={'base_template': 'textarea.html'})
    taxon_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DBtables.Species


class EnsemblGeneSerializer(serializers.Serializer):
    ensembl_gene_id = serializers.IntegerField(read_only=True)
    species_id = serializers.IntegerField(read_only=True)
    ensembl_stable_id = serializers.CharField(style={'base_template': 'textarea.html'})
    scientific_name = serializers.CharField(allow_null=True, source='species.scientific_name')

    class Meta:
        model = DBtables.EnsemblGene
