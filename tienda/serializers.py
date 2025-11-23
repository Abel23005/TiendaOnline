from rest_framework import serializers
from .models import Categoria, Producto, CartItem

class CategoriaSerializer(serializers.ModelSerializer):
    productos_count = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'activa', 'productos_count']

    def get_productos_count(self, obj):
        return obj.productos.filter(activo=True).count()

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    disponible = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_nombre', 
                 'imagen', 'stock', 'activo', 'disponible', 'fecha_creacion']

class ProductoDetalleSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    disponible = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'imagen', 
                 'stock', 'activo', 'disponible', 'fecha_creacion', 'fecha_actualizacion']


class CartItemSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.filter(activo=True),
        source='producto',
        write_only=True
    )
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'producto', 'producto_id', 'cantidad', 'subtotal']

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor que cero.')
        return value

    def validate(self, attrs):
        producto = attrs.get('producto') or getattr(self.instance, 'producto', None)
        cantidad = attrs.get('cantidad') or getattr(self.instance, 'cantidad', None)
        if producto and cantidad and cantidad > producto.stock:
            raise serializers.ValidationError('No hay stock suficiente para la cantidad solicitada.')
        return attrs


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_items = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)

