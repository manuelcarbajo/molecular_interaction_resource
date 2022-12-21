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
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('species_id/<int:species_id>/', views.species_id, name='species_id'),
    path('source_dbs/', views.source_dbs, name='source_dbs'),
    path('species/', views.species, name='species'),
    path('ensembl_gene/', views.ensembl_gene, name='ensembl_gene'),
    path('interactions_by_prodname/', views.interactions_by_prodname, name='interactions_by_prodname'),
    path('display_by_gene/<str:ens_stbl_id>/', views.display_by_gene, name='display_by_gene'),
    path('display_by_gene/<str:ens_stbl_id>', views.display_by_gene, name='display_by_gene'),
    re_path(r'^.*$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger_ui'),
    ]

