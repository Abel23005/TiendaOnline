from rest_framework import serializers
from .models import Categoria, Producto

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
