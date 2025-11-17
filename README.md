# Sistema de Ecommerce Django

Un sistema completo de ecommerce desarrollado en Django con API REST y interfaz web moderna.

## Características

- ✅ **5 Categorías de productos**: Zapatería, Pastelería, Mueblería, Juegos de Mesa, Útiles Escolares
- ✅ **Gestión de productos**: Cada categoría tiene mínimo 4 productos
- ✅ **API REST completa** con Django REST Framework
- ✅ **Vista Home**: Listado de todos los productos
- ✅ **Vista DetalleProducto**: Información detallada del producto
- ✅ **Vista Carrito**: Gestión de productos (sin compra real)
- ✅ **Interfaz moderna** con TailwindCSS
- ✅ **Responsive design**
- ✅ **Funcionalidad de carrito** con localStorage

## Estructura del Proyecto

```
lab13/
├── ecommerce/              # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tienda/                 # Aplicación principal
│   ├── models.py          # Modelos Categoria y Producto
│   ├── views.py           # Vistas API y templates
│   ├── serializers.py     # Serializers para API
│   ├── urls.py            # URLs de la aplicación
│   ├── admin.py           # Configuración del admin
│   └── management/commands/
│       └── poblar_datos.py # Comando para poblar BD
├── templates/              # Plantillas HTML
│   ├── base.html
│   └── tienda/
│       ├── home.html
│       ├── detalle_producto.html
│       └── carrito.html
├── requirements.txt        # Dependencias
└── manage.py
```

## Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 4. Poblar la base de datos

```bash
python manage.py poblar_datos
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

## URLs Principales

### Interfaz Web
- **Home**: `http://localhost:8000/` - Página principal con productos destacados
- **Detalle Producto**: `http://localhost:8000/producto/<id>/` - Información detallada
- **Carrito**: `http://localhost:8000/carrito/` - Gestión del carrito de compras
- **Admin**: `http://localhost:8000/admin/` - Panel de administración

### API REST
- **Categorías**: `http://localhost:8000/api/categorias/` - Lista todas las categorías
- **Productos**: `http://localhost:8000/api/productos/` - Lista todos los productos
- **Producto Detalle**: `http://localhost:8000/api/productos/<id>/` - Detalle de un producto
- **Productos por Categoría**: `http://localhost:8000/api/categorias/<id>/productos/` - Productos de una categoría

### Funcionalidades de la API
- **Búsqueda**: `?search=término` - Buscar productos por nombre o descripción
- **Ordenamiento**: `?ordering=precio` o `?ordering=-fecha_creacion`

## Modelos

### Categoria
- `nombre`: Nombre de la categoría
- `descripcion`: Descripción de la categoría
- `imagen`: Imagen de la categoría (opcional)
- `activa`: Estado de la categoría
- `fecha_creacion`: Fecha de creación

### Producto
- `nombre`: Nombre del producto
- `descripcion`: Descripción detallada
- `precio`: Precio del producto
- `categoria`: Relación con Categoria
- `imagen`: Imagen del producto (opcional)
- `stock`: Cantidad disponible
- `activo`: Estado del producto
- `fecha_creacion`: Fecha de creación
- `fecha_actualizacion`: Última actualización

## Categorías y Productos Incluidos

### 🥿 Zapatería (4 productos)
- Zapatillas Nike Air Max - $89.99
- Botas de Cuero Clásicas - $129.99
- Sandalias de Verano - $34.99
- Zapatos de Vestir Oxford - $149.99

### 🧁 Pastelería (4 productos)
- Torta de Chocolate Premium - $45.00
- Cupcakes Variados (6 unidades) - $18.50
- Cheesecake de Frutos Rojos - $38.00
- Macarons Franceses (12 unidades) - $24.99

### 🪑 Mueblería (4 productos)
- Sofá de 3 Plazas Moderno - $599.99
- Mesa de Comedor de Roble - $449.99
- Estantería Modular - $129.99
- Silla Ergonómica de Oficina - $189.99

### 🎲 Juegos de Mesa (4 productos)
- Monopoly Edición Clásica - $29.99
- Scrabble Deluxe - $39.99
- Ajedrez de Madera Tallada - $79.99
- UNO Cartas Originales - $12.99

### 📚 Útiles Escolares y de Oficina (4 productos)
- Set de Lápices de Colores (48 colores) - $24.99
- Calculadora Científica - $34.99
- Cuadernos Universitarios (Pack 5) - $15.99
- Mochila Escolar Resistente - $49.99

## Funcionalidades del Carrito

- ✅ Agregar productos al carrito
- ✅ Modificar cantidades
- ✅ Eliminar productos
- ✅ Cálculo automático de totales
- ✅ Persistencia con localStorage
- ✅ Contador de productos en navegación
- ✅ Simulación de checkout

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Frontend**: HTML5, TailwindCSS, JavaScript (Vanilla)
- **Base de Datos**: SQLite (desarrollo)
- **Iconos**: Font Awesome 6.0
- **Estilos**: TailwindCSS (CDN)

## Comandos Útiles

```bash
# Ver todos los productos
python manage.py shell
>>> from tienda.models import Producto
>>> Producto.objects.all()

# Limpiar y repoblar datos
python manage.py flush
python manage.py poblar_datos

# Crear migraciones después de cambios en modelos
python manage.py makemigrations tienda
python manage.py migrate
```

## Notas de Desarrollo

- El proyecto está configurado para desarrollo con `DEBUG = True`
- Las imágenes se almacenan en `media/` (crear carpeta si es necesario)
- El carrito funciona con localStorage (no requiere autenticación)
- Los errores de lint en templates son normales (sintaxis Django vs JavaScript)

## Próximas Mejoras

- [ ] Sistema de autenticación de usuarios
- [ ] Procesamiento real de pagos
- [ ] Sistema de reviews y calificaciones
- [ ] Filtros avanzados por categoría
- [ ] Wishlist/Lista de deseos
- [ ] Sistema de cupones y descuentos
