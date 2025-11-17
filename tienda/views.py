from django.shortcuts import render, get_object_or_404
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer, ProductoDetalleSerializer

# API Views
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer

class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['categoria']  # Requiere django-filter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'fecha_creacion']
    ordering = ['-fecha_creacion']

class ProductoDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoDetalleSerializer

@api_view(['GET'])
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activa=True)
    productos = Producto.objects.filter(categoria=categoria, activo=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response({
        'categoria': CategoriaSerializer(categoria).data,
        'productos': serializer.data
    })

# Template Views
def home(request):
    categorias = Categoria.objects.filter(activa=True)
    productos_destacados = Producto.objects.filter(activo=True)[:8]
    context = {
        'categorias': categorias,
        'productos': productos_destacados,
        'titulo': 'Tienda Online - Inicio'
    }
    return render(request, 'tienda/home.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'titulo': f'{producto.nombre} - Detalle'
    }
    return render(request, 'tienda/detalle_producto.html', context)

def carrito(request):
    context = {
        'titulo': 'Carrito de Compras'
    }
    return render(request, 'tienda/carrito.html', context)
