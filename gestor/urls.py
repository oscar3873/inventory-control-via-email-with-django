from django.urls import path
from gestor import views

urlpatterns = [
    path('home',views.index, name='home'),
    path('',views.index, name='home'),
    path('productos/',views.ProductoListView.list_productos, name='productos'),
    path('configurar/',views.configurar, name='configurar'),
    path('producto/new/', views.producto_new, name='producto_new'),
    path('producto/update/<pk>', views.producto_update, name='producto_update'),
    path('producto/<pk>/delete/', views.ProductoListView.producto_delete, name='producto_delete'),
    path('vencimientos/',views.VencimientoListView.productos_vencimiento, name='vencimientos'),
    path('registrar/',views.registrar, name='registrar'),
    path('logout/',views.signout, name='logout'),
    path('producto/<busqueda>/',views.Buscar, name='productos_filt'),
    path('signin/',views.signin, name='signin'),
    # path('productos/proximos_a_vencer_', views.ProductosListView.productos_list, name='proximos_a_vencer'),
    # path('producto/<pk>', views.ProductoDetailView.as_view(), name='producto'),
    # path('producto/new/', views.ProductosListView.producto_new, name='producto_new'),
    # path('producto/editar/', views.ProductoDetailView.producto_editar, name='producto_editar'),
    # path('settings/', views.SettingsView.as_view(), name='settings'),
]