from django.contrib import admin
import home.models as DBtables


@admin.register(DBtables.Species)
class SpeciesAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.CuratedInteractor)
class CuratedInteractorAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.PredictionMethod)
class PredictionMethodAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.EnsemblGene)
class EnsemblGeneAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.SourceDb)
class SourceDbAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.MetaKey)
class MetaKeyAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.Ontology)
class OntologyAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.OntologyTerm)
class OntologyTermAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.PredictedInteractor)
class PredictedInteractorAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.Interaction)
class InteractionAdmin(admin.ModelAdmin):
	pass

@admin.register(DBtables.KeyValuePair)
class KeyValuePairAdmin(admin.ModelAdmin):
	pass
