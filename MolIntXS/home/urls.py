from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter


from home import views

router = DefaultRouter(trailing_slash=False)

router.register(r'prodname_ensgene/(?P<ens_gene>[^/.]+)/(?P<prod_name>[^/.]+)/', views.InteractionsForEnsgeneProdnameViewSet, basename='prodname_ensgene')

urlpatterns = [
    path('', views.index, name='index'),
    path('species_id/<int:species_id>/', views.species_id, name='species_id'),
    path('species/', views.species, name='species'),
    path('ensembl_gene/', views.ensembl_gene, name='ensembl_gene'),
    path('interactions_by_prodname/', views.interactions_by_prodname, name='interactions_by_prodname'),
    path('display_by_gene/<str:ens_stbl_id>/', views.display_by_gene, name='display_by_gene'),
    #path('prodname_ensgene/<ens_gene>/<prod_name>/', views.InteractionsForEnsgeneProdnameViewSet.as_view(), name='prodname_ensgene'),
    re_path(r'^ensweb/', include((router.urls, 'ensweb'), namespace='ensweb')),
]