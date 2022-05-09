from rest_framework import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models import Species

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Species):
            return str(obj)
        return super().default(obj)



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