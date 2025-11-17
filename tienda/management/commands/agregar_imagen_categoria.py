import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from tienda.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Agregar imagen a una categoría específica desde URL'

    def add_arguments(self, parser):
        parser.add_argument('categoria', type=str, help='Nombre de la categoría')
        parser.add_argument('url', type=str, help='URL de la imagen')

    def handle(self, *args, **options):
        categoria_nombre = options['categoria']
        imagen_url = options['url']
        
        self.stdout.write(f'Descargando imagen para categoría: {categoria_nombre}')
        
        try:
            categoria = Categoria.objects.get(nombre=categoria_nombre)
            
            # Descargar imagen
            response = requests.get(imagen_url, timeout=10)
            if response.status_code == 200:
                # Asignar imagen a la categoría
                imagen_nombre = f"{categoria_nombre.lower().replace(' ', '_').replace('í', 'i').replace('é', 'e')}.jpg"
                categoria.imagen.save(
                    imagen_nombre,
                    ContentFile(response.content),
                    save=True
                )
                self.stdout.write(f'✓ Imagen asignada a categoría: {categoria_nombre}')
                
                # Asignar la misma imagen a todos los productos de la categoría
                productos = Producto.objects.filter(categoria=categoria)
                for producto in productos:
                    producto_imagen_nombre = f"{producto.nombre.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('í', 'i').replace('é', 'e')}.jpg"
                    producto.imagen.save(
                        producto_imagen_nombre,
                        ContentFile(response.content),
                        save=True
                    )
                    self.stdout.write(f'✓ Imagen asignada a producto: {producto.nombre}')
                    
                self.stdout.write(self.style.SUCCESS(f'¡Imagen procesada exitosamente para {categoria_nombre}!'))
            else:
                self.stdout.write(f'✗ Error descargando imagen: {response.status_code}')
                
        except Categoria.DoesNotExist:
            self.stdout.write(f'✗ Categoría no encontrada: {categoria_nombre}')
            self.stdout.write('Categorías disponibles:')
            for cat in Categoria.objects.all():
                self.stdout.write(f'  - {cat.nombre}')
        except Exception as e:
            self.stdout.write(f'✗ Error procesando imagen: {str(e)}')
