from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # Template URLs
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    
    # API URLs
    path('api/categorias/', views.CategoriaListView.as_view(), name='api_categorias'),
    path('api/productos/', views.ProductoListView.as_view(), name='api_productos'),
    path('api/productos/<int:pk>/', views.ProductoDetailView.as_view(), name='api_producto_detalle'),
    path('api/categorias/<int:categoria_id>/productos/', views.productos_por_categoria, name='api_productos_categoria'),
    path('api/carrito/procesar-pago/', views.procesar_pago, name='api_procesar_pago'),
]
