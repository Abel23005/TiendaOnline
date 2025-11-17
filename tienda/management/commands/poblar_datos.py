from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Poblar la base de datos con categorías y productos de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write('Poblando base de datos...')
        
        # Crear categorías
        categorias_data = [
            {
                'nombre': 'Zapatería',
                'descripcion': 'Calzado para toda la familia, desde deportivos hasta elegantes zapatos de vestir.'
            },
            {
                'nombre': 'Pastelería',
                'descripcion': 'Deliciosos pasteles, tortas y postres artesanales para toda ocasión.'
            },
            {
                'nombre': 'Mueblería',
                'descripcion': 'Muebles de calidad para el hogar, oficina y espacios comerciales.'
            },
            {
                'nombre': 'Juegos de Mesa',
                'descripcion': 'Entretenimiento familiar con los mejores juegos de mesa y cartas.'
            },
            {
                'nombre': 'Útiles Escolares y de Oficina',
                'descripcion': 'Todo lo necesario para el estudio y trabajo, desde lápices hasta equipos de oficina.'
            }
        ]

        categorias = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias[cat_data['nombre']] = categoria
            if created:
                self.stdout.write(f'✓ Categoría creada: {categoria.nombre}')

        # Crear productos
        productos_data = [
            # Zapatería
            {'nombre': 'Zapatillas Nike Air Max', 'descripcion': 'Zapatillas deportivas cómodas y elegantes, perfectas para correr y uso diario.', 'precio': Decimal('89.99'), 'categoria': 'Zapatería', 'stock': 25},
            {'nombre': 'Botas de Cuero Clásicas', 'descripcion': 'Botas de cuero genuino, ideales para ocasiones formales y uso profesional.', 'precio': Decimal('129.99'), 'categoria': 'Zapatería', 'stock': 15},
            {'nombre': 'Sandalias de Verano', 'descripcion': 'Sandalias cómodas y frescas, perfectas para la temporada de calor.', 'precio': Decimal('34.99'), 'categoria': 'Zapatería', 'stock': 30},
            {'nombre': 'Zapatos de Vestir Oxford', 'descripcion': 'Elegantes zapatos Oxford de cuero, ideales para eventos formales.', 'precio': Decimal('149.99'), 'categoria': 'Zapatería', 'stock': 12},

            # Pastelería
            {'nombre': 'Torta de Chocolate Premium', 'descripcion': 'Deliciosa torta de chocolate con cobertura de ganache y decoración artesanal.', 'precio': Decimal('45.00'), 'categoria': 'Pastelería', 'stock': 8},
            {'nombre': 'Cupcakes Variados (6 unidades)', 'descripcion': 'Set de 6 cupcakes con diferentes sabores: vainilla, chocolate, fresa y limón.', 'precio': Decimal('18.50'), 'categoria': 'Pastelería', 'stock': 20},
            {'nombre': 'Cheesecake de Frutos Rojos', 'descripcion': 'Cremoso cheesecake con base de galleta y topping de frutos rojos frescos.', 'precio': Decimal('38.00'), 'categoria': 'Pastelería', 'stock': 10},
            {'nombre': 'Macarons Franceses (12 unidades)', 'descripcion': 'Elegantes macarons franceses en sabores variados, presentación de lujo.', 'precio': Decimal('24.99'), 'categoria': 'Pastelería', 'stock': 15},

            # Mueblería
            {'nombre': 'Sofá de 3 Plazas Moderno', 'descripcion': 'Cómodo sofá de 3 plazas con tapizado en tela resistente y diseño contemporáneo.', 'precio': Decimal('599.99'), 'categoria': 'Mueblería', 'stock': 5},
            {'nombre': 'Mesa de Comedor de Roble', 'descripcion': 'Elegante mesa de comedor en madera de roble macizo para 6 personas.', 'precio': Decimal('449.99'), 'categoria': 'Mueblería', 'stock': 3},
            {'nombre': 'Estantería Modular', 'descripcion': 'Estantería modular de 5 niveles, perfecta para libros y decoración.', 'precio': Decimal('129.99'), 'categoria': 'Mueblería', 'stock': 8},
            {'nombre': 'Silla Ergonómica de Oficina', 'descripcion': 'Silla de oficina con soporte lumbar y ajuste de altura, ideal para trabajo prolongado.', 'precio': Decimal('189.99'), 'categoria': 'Mueblería', 'stock': 12},

            # Juegos de Mesa
            {'nombre': 'Monopoly Edición Clásica', 'descripcion': 'El clásico juego de bienes raíces para toda la familia, horas de diversión garantizada.', 'precio': Decimal('29.99'), 'categoria': 'Juegos de Mesa', 'stock': 20},
            {'nombre': 'Scrabble Deluxe', 'descripcion': 'Juego de palabras premium con tablero giratorio y fichas de madera.', 'precio': Decimal('39.99'), 'categoria': 'Juegos de Mesa', 'stock': 15},
            {'nombre': 'Ajedrez de Madera Tallada', 'descripcion': 'Elegante set de ajedrez con piezas talladas a mano y tablero de madera noble.', 'precio': Decimal('79.99'), 'categoria': 'Juegos de Mesa', 'stock': 8},
            {'nombre': 'UNO Cartas Originales', 'descripcion': 'El famoso juego de cartas UNO, diversión rápida para toda la familia.', 'precio': Decimal('12.99'), 'categoria': 'Juegos de Mesa', 'stock': 35},

            # Útiles Escolares y de Oficina
            {'nombre': 'Set de Lápices de Colores (48 colores)', 'descripcion': 'Caja de lápices de colores profesionales con 48 tonos vibrantes.', 'precio': Decimal('24.99'), 'categoria': 'Útiles Escolares y de Oficina', 'stock': 25},
            {'nombre': 'Calculadora Científica', 'descripcion': 'Calculadora científica con funciones avanzadas, ideal para estudiantes y profesionales.', 'precio': Decimal('34.99'), 'categoria': 'Útiles Escolares y de Oficina', 'stock': 18},
            {'nombre': 'Cuadernos Universitarios (Pack 5)', 'descripcion': 'Pack de 5 cuadernos universitarios de 100 hojas cada uno, rayado y cuadriculado.', 'precio': Decimal('15.99'), 'categoria': 'Útiles Escolares y de Oficina', 'stock': 30},
            {'nombre': 'Mochila Escolar Resistente', 'descripcion': 'Mochila escolar con múltiples compartimentos, resistente al agua y ergonómica.', 'precio': Decimal('49.99'), 'categoria': 'Útiles Escolares y de Oficina', 'stock': 20},
        ]

        for prod_data in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'descripcion': prod_data['descripcion'],
                    'precio': prod_data['precio'],
                    'categoria': categorias[prod_data['categoria']],
                    'stock': prod_data['stock']
                }
            )
            if created:
                self.stdout.write(f'✓ Producto creado: {producto.nombre}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Datos poblados exitosamente!\n'
                f'Categorías: {Categoria.objects.count()}\n'
                f'Productos: {Producto.objects.count()}'
            )
        )
