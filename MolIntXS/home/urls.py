from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from home import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    path('species', views.species, name='species'),
    path('meta_values', views.meta_values, name='meta_values'),
    path('interactions', views.interactions, name='interactions'),
    path('meta_keys', views.meta_keys, name='meta_keys'),
    path('species/by_species_id/<int:species_id>', views.species_id, name='species_id'),
    path('species/by_ensembl_name/<str:species_production_name>', views.species_by_ensembl_name, name='species_by_ensembl_name'),
    path('species/by_scientific_name/<str:species_scientific_name>', views.species_by_scientific_name, name='species_by_scientific_name'),
    path('source_dbs', views.source_dbs, name='source_dbs'),
    path('ensembl_gene', views.ensembl_gene, name='ensembl_gene'),
    path('interactions_by_prodname', views.interactions_by_prodname, name='interactions_by_prodname'),
    path('interactors/by_ensembl_name', views.interactors_by_prodname, name='interactors_by_prodname'),
    path('interactors/by_ensembl_name/<str:species_production_name>', views.interactors_by_specific_prodname, name='interactors_by_specific_prodname'),
    path('interactors/by_scientific_name/<str:species_scientific_name>', views.interactors_by_specific_scientific_name, name='interactors_by_specific_scientific_name'),
    path('display_by_gene/<str:ens_stbl_id>', views.display_by_gene, name='display_by_gene'),
    re_path(r'^.*$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger_ui'),
    ]

