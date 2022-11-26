from gestor.views import configurar, index
from django.urls import path
from gestor import views

urlpatterns = [
    path('home',index, name='home'),
    path('',index, name='home'),
    path('productos/',views.ProductoListView.as_view(), name='productos'),
    path('configurar/',configurar, name='configurar'),
    # path('productos/proximos_a_vencer_', views.ProductosListView.productos_list, name='proximos_a_vencer'),
    # path('producto/<pk>', views.ProductoDetailView.as_view(), name='producto'),
    # path('producto/new/', views.ProductosListView.producto_new, name='producto_new'),
    # path('producto/delete/', views.ProductosListView.producto_delete, name='producto_delete'),
    # path('producto/editar/', views.ProductoDetailView.producto_editar, name='producto_editar'),
    # path('settings/', views.SettingsView.as_view(), name='settings'),
]