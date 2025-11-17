import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from tienda.models import Producto

class Command(BaseCommand):
    help = 'Agregar imagen a un producto específico desde URL'

    def add_arguments(self, parser):
        parser.add_argument('producto', type=str, help='Nombre del producto')
        parser.add_argument('url', type=str, help='URL de la imagen')

    def handle(self, *args, **options):
        producto_nombre = options['producto']
        imagen_url = options['url']
        
        self.stdout.write(f'Descargando imagen para producto: {producto_nombre}')
        
        try:
            producto = Producto.objects.get(nombre=producto_nombre)
            
            # Descargar imagen
            response = requests.get(imagen_url, timeout=15)
            if response.status_code == 200:
                # Asignar imagen al producto
                producto_imagen_nombre = f"{producto.nombre.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('í', 'i').replace('é', 'e')}.jpg"
                producto.imagen.save(
                    producto_imagen_nombre,
                    ContentFile(response.content),
                    save=True
                )
                self.stdout.write(f'✓ Imagen asignada a producto: {producto.nombre}')
                self.stdout.write(self.style.SUCCESS(f'¡Imagen procesada exitosamente para {producto_nombre}!'))
            else:
                self.stdout.write(f'✗ Error descargando imagen: {response.status_code}')
                
        except Producto.DoesNotExist:
            self.stdout.write(f'✗ Producto no encontrado: {producto_nombre}')
            self.stdout.write('Productos disponibles:')
            for prod in Producto.objects.all():
                self.stdout.write(f'  - {prod.nombre}')
        except Exception as e:
            self.stdout.write(f'✗ Error procesando imagen: {str(e)}')
