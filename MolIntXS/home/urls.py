from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from home import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

#router = DefaultRouter(trailing_slash=False)
schema_view = get_schema_view(
    openapi.Info(
        title="API interactions doc",
        default_version='v1',
        description="Ensembl Interactions REST API\nA list of endpoints to provide access to the Ensembl molecular interactions database.\nWe welcome your suggestions to add endpoints to fit new use case scenarios. Please write to helpdesk@ensemblgenomes.org",
    ),
    url='https://interactions.rest.ensembl.org',
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('meta_data',views.KeyValuePairList.as_view(),name='metadataList'),
    path('meta_values', views.meta_values, name='meta_values'),
    path('meta_keys', views.meta_keys, name='meta_keys'),

    path('interaction', views.InteractionList.as_view(), name='interactionList'),
    #path('interaction/interactor_id/<int:interactor_id>', views.interactions_by_interactor_id, name='interactions_by_any_interactor'),
    #path('interaction/meta_key/<str:meta_key>', views.interactions_by_meta_key, name='interactions_by_meta_key'),
    #path('interaction/meta_value/<str:meta_value>', views.interactions_by_meta_value, name='interactions_by_meta_value'),
    #path('interaction/meta_key/<str:meta_key>/meta_value/<str:meta_value>', views.interactions_by_meta_key_meta_value, name='interactions_by_meta_key_meta_value'),
    
    path('species', views.SpeciesList.as_view(), name='speciesList'),
    #path('species/species_id/<int:species_id>', views.species_id, name='species_id'),
    #path('species/ensembl_name/<str:species_production_name>', views.species_by_ensembl_name, name='species_by_ensembl_name'),
    #path('species/scientific_name/<str:species_scientific_name>', views.species_by_scientific_name, name='species_by_scientific_name'),
    
    path('source_dbs', views.source_dbs, name='source_dbs'),
    
    path('ensembl_gene', views.EnsemblGeneList.as_view(), name='ensembl_geneList'),
    path('ensembl_gene/ensembl_name', views.ensembl_gene_by_prodname, name='ens_genes_by_prodname'),
    #path('ensembl_gene/ensembl_name/<str:species_production_name>', views.ensembl_gene_by_specific_prodname, name='ensembl_gene_by_specific_prodname'),
    #path('ensembl_gene/scientific_name/<str:species_scientific_name>', views.ensembl_gene_by_specific_scientific_name, name='ensembl_gene_by_specific_scientific_name'),
    
    path('interactor', views.CuratedInteractorList.as_view(), name='interactorList'),
    #path('interactor/name/<str:interactor_name>', views.interactor_name, name='interactorList'),
    #path('interactor/ensembl_gene/<str:ensembl_gene>', views.interactor_ensembl_gene, name='interactor_ensembl_gene'),
    #path('interactor/production_name/<str:production_name>', views.interactor_by_specific_prodname, name='interactors_by_prod_name'),
    #path('interactor/scientific_name/<str:scientific_name>', views.interactor_by_scientific_name, name='interactors_by_scientific_name'),
    #path('interactor/interactor_id/<int:curated_interactor_id>', views.interactor_id, name='interactor_id'),

    #USED BY WEB!
    path('interactor/ensembl_name', views.interactors_by_prodname, name='interactors_by_prodname'),
    path('interactions_by_prodname', views.interactions_by_prodname, name='interactions_by_prodname'),
    path('display_by_gene/<str:ens_stbl_id>', views.display_by_gene, name='display_by_gene'),
    
    re_path(r'^.*$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger_ui'),
    ]

