import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from tienda.models import Categoria, Producto
from django.conf import settings

class Command(BaseCommand):
    help = 'Agregar imágenes a productos desde URLs'

    def handle(self, *args, **options):
        self.stdout.write('Descargando y asignando imágenes...')
        
        # URLs de imágenes por categoría
        imagenes = {
            'Zapatería': {
                'url': 'https://tse2.mm.bing.net/th/id/OIP.oCqRZ2v3Asm6aPNIR_K53gHaEK?rs=1&pid=ImgDetMain&o=7&rm=3',
                'productos': ['Zapatillas Nike Air Max', 'Botas de Cuero Clásicas', 'Sandalias de Verano', 'Zapatos de Vestir Oxford']
            }
        }
        
        for categoria_nombre, data in imagenes.items():
            try:
                categoria = Categoria.objects.get(nombre=categoria_nombre)
                
                # Descargar imagen
                response = requests.get(data['url'], timeout=10)
                if response.status_code == 200:
                    # Asignar imagen a la categoría
                    imagen_nombre = f"{categoria_nombre.lower().replace(' ', '_')}.jpg"
                    categoria.imagen.save(
                        imagen_nombre,
                        ContentFile(response.content),
                        save=True
                    )
                    self.stdout.write(f'✓ Imagen asignada a categoría: {categoria_nombre}')
                    
                    # Asignar la misma imagen a todos los productos de la categoría
                    for producto_nombre in data['productos']:
                        try:
                            producto = Producto.objects.get(nombre=producto_nombre)
                            producto_imagen_nombre = f"{producto_nombre.lower().replace(' ', '_').replace('(', '').replace(')', '')}.jpg"
                            producto.imagen.save(
                                producto_imagen_nombre,
                                ContentFile(response.content),
                                save=True
                            )
                            self.stdout.write(f'✓ Imagen asignada a producto: {producto_nombre}')
                        except Producto.DoesNotExist:
                            self.stdout.write(f'✗ Producto no encontrado: {producto_nombre}')
                else:
                    self.stdout.write(f'✗ Error descargando imagen para {categoria_nombre}: {response.status_code}')
                    
            except Categoria.DoesNotExist:
                self.stdout.write(f'✗ Categoría no encontrada: {categoria_nombre}')
            except Exception as e:
                self.stdout.write(f'✗ Error procesando {categoria_nombre}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('¡Imágenes procesadas exitosamente!'))
