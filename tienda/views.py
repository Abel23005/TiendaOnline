from django.shortcuts import render, get_object_or_404
from django.db import transaction
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Producto, Compra, DetalleCompra
from .serializers import CategoriaSerializer, ProductoSerializer, ProductoDetalleSerializer, CompraSerializer

# API Views
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['categoria']  # Requiere django-filter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProductoDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoDetalleSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['GET'])
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activa=True)
    productos = Producto.objects.filter(categoria=categoria, activo=True)
    categoria_serializer = CategoriaSerializer(categoria, context={'request': request})
    productos_serializer = ProductoSerializer(productos, many=True, context={'request': request})
    return Response({
        'categoria': categoria_serializer.data,
        'productos': productos_serializer.data
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

def mis_compras(request):
    compras = Compra.objects.all().order_by('-fecha').prefetch_related('detalles__producto')
    
    # Calcular estadísticas
    total_gastado = sum(compra.total for compra in compras)
    total_productos = sum(detalle.cantidad for compra in compras for detalle in compra.detalles.all())
    
    context = {
        'compras': compras,
        'titulo': 'Mis Compras',
        'total_gastado': total_gastado,
        'total_productos': total_productos,
        'total_compras': compras.count()
    }
    return render(request, 'tienda/mis_compras.html', context)

@api_view(['POST'])
@transaction.atomic
def procesar_pago(request):
    """
    Procesa el pago de una compra, valida stock, crea la compra y actualiza inventario
    """
    try:
        cart_items = request.data.get('items', [])
        
        if not cart_items:
            return Response(
                {'error': 'El carrito está vacío'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar stock y calcular totales
        subtotal = Decimal('0.00')
        detalles_data = []
        
        for item in cart_items:
            producto_id = item.get('id')
            cantidad = int(item.get('quantity', 0))
            precio = Decimal(str(item.get('price', 0)))
            
            if cantidad <= 0:
                continue
            
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            
            # Validar stock disponible
            if producto.stock < cantidad:
                return Response(
                    {
                        'error': f'Stock insuficiente para {producto.nombre}. Stock disponible: {producto.stock}, solicitado: {cantidad}'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            item_subtotal = precio * cantidad
            subtotal += item_subtotal
            
            detalles_data.append({
                'producto': producto,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'subtotal': item_subtotal
            })
        
        if subtotal == 0:
            return Response(
                {'error': 'No se puede procesar una compra sin items válidos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular costos adicionales
        envio = Decimal('5.00')
        impuestos = subtotal * Decimal('0.10')  # 10% de impuestos
        total = subtotal + envio + impuestos
        
        # Crear la compra
        compra = Compra.objects.create(
            subtotal=subtotal,
            envio=envio,
            impuestos=impuestos,
            total=total,
            estado='completada'
        )
        
        # Crear detalles y actualizar stock
        for detalle_data in detalles_data:
            producto = detalle_data['producto']
            
            # Crear detalle de compra
            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=detalle_data['cantidad'],
                precio_unitario=detalle_data['precio_unitario'],
                subtotal=detalle_data['subtotal']
            )
            
            # Actualizar stock
            producto.stock -= detalle_data['cantidad']
            producto.save()
        
        # Serializar respuesta
        serializer = CompraSerializer(compra)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error al procesar el pago: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
