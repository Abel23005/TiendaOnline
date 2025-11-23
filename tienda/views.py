from django.shortcuts import render, get_object_or_404
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Producto, CartItem
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ProductoDetalleSerializer,
    CartItemSerializer,
    CartSerializer,
)

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


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


@api_view(['GET', 'POST'])
def cart_list_create(request):
    session_key = _get_session_key(request)

    if request.method == 'GET':
        items = CartItem.objects.filter(session_key=session_key).select_related('producto')
        subtotal = sum((item.subtotal for item in items), 0)
        serializer = CartSerializer({
            'items': items,
            'total_items': items.count(),
            'subtotal': subtotal,
        })
        return Response(serializer.data)

    # POST: agregar producto o incrementar cantidad
    data = request.data.copy()
    producto_id = data.get('producto_id') or data.get('producto')
    cantidad = int(data.get('cantidad', 1))

    try:
        producto = Producto.objects.get(pk=producto_id, activo=True)
    except (Producto.DoesNotExist, TypeError, ValueError):
        return Response({'detail': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        producto=producto,
        defaults={'cantidad': 0},
    )
    nueva_cantidad = item.cantidad + cantidad

    serializer = CartItemSerializer(instance=item, data={'cantidad': nueva_cantidad}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
def cart_item_detail(request, pk):
    session_key = _get_session_key(request)
    try:
        item = CartItem.objects.select_related('producto').get(pk=pk, session_key=session_key)
    except CartItem.DoesNotExist:
        return Response({'detail': 'Ítem no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH: actualizar cantidad
    cantidad = request.data.get('cantidad')
    if cantidad is None:
        return Response({'detail': 'Debe proporcionar la cantidad.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CartItemSerializer(instance=item, data={'cantidad': cantidad}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

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
