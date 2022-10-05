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
    prod_name = serializers.CharField(source='ensembl_gene.species.production_name')
    division = serializers.CharField(source='ensembl_gene.species.ensembl_division')
    ens_gene = serializers.CharField(source='ensembl_gene.ensembl_stable_id')
    curies =serializers.CharField(read_only=True)
    interactor_type = serializers.CharField()


    class Meta:
        model = DBtables.CuratedInteractor


class InteractionSerializer(serializers.Serializer):
    label = serializers.CharField(source='source_db.label')
    interactor_1 = CuratedInteractorSerializer()
    interactor_2 = CuratedInteractorSerializer()

    class Meta:
        model = DBtables.Interaction

class SpeciesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ensembl_division = serializers.CharField(required=True, allow_blank=False, max_length=255)
    production_name = serializers.CharField(style={'base_template': 'textarea.html'})
    taxon_id = serializers.IntegerField(read_only=True)


    def create(self, validated_data):
        """
        Create and return a new `Species` instance, given the validated data.
        """
        return Species.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Species` instance, given the validated data.
        """
        instance.ensembl_division = validated_data.get('ensembl_division', instance.ensembl_division)
        instance.production_name = validated_data.get('production_name', instance.production_name)
        instance.taxon_id = validated_data.get('taxon_id', instance.taxon_id)
    
        instance.save()
        return instance


class EnsemblGeneSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    species_id = serializers.IntegerField(read_only=True)
    ensembl_stable_id = serializers.CharField(style={'base_template': 'textarea.html'})
    import_timestamp = serializers.DateTimeField()


    def create(self, validated_data):
        """
        Create and return a new `EnsemblGene` instance, given the validated data.
        """
        return EnsemblGene.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `EnsemblGene` instance, given the validated data.
        """
        instance.species_id = validated_data.get('species_id', instance.species_id)
        instance.ensembl_stable_id = validated_data.get('ensembl_stable_id', instance.ensembl_stable_id)
        instance.import_timestamp = validated_data.get('import_timestamp', instance.import_timestamp)
    
        instance.save()
        return instance