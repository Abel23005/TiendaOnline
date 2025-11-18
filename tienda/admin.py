from django.contrib import admin
from .models import Categoria, Producto, Compra, DetalleCompra

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre']
    list_editable = ['activa']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    readonly_fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    extra = 0

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    readonly_fields = ['fecha', 'subtotal', 'envio', 'impuestos', 'total']
    inlines = [DetalleCompraInline]
    
    def has_add_permission(self, request):
        return False
