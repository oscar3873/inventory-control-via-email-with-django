from gestor.views import configurar, index
from django.urls import path
from gestor import views

urlpatterns = [
    path('home',index, name='home'),
    path('',index, name='home'),
    path('productos/',views.ProductoListView.Buscar, name='productos'),
    path('configurar/',configurar, name='configurar'),
    path('producto/new/', views.producto_new, name='producto_new'),
    path('producto/update/<pk>', views.producto_update, name='producto_update'),
    path('producto/<pk>/delete/', views.ProductoListView.producto_delete, name='producto_delete'),
    path('vencimientos/',views.VencimientoListView.Buscar, name='vencimientos'),
    # path('productos/proximos_a_vencer_', views.ProductosListView.productos_list, name='proximos_a_vencer'),
    # path('producto/<pk>', views.ProductoDetailView.as_view(), name='producto'),
    # path('producto/new/', views.ProductosListView.producto_new, name='producto_new'),
    # path('producto/editar/', views.ProductoDetailView.producto_editar, name='producto_editar'),
    # path('settings/', views.SettingsView.as_view(), name='settings'),
]