import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { useProducts, useAddToCart, useCategories } from '../api/hooks';

export default function Home() {
  const { data: productosData, isLoading: loadingProductos } = useProducts();
  const { data: categoriasData, isLoading: loadingCategorias } = useCategories();
  const addToCart = useAddToCart();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  if (loadingProductos || loadingCategorias) {
    return <div className="text-center py-10">Cargando contenido...</div>;
  }

  const productos = productosData || [];
  const categorias = categoriasData || [];

  return (
    <div className="min-h-screen">
      {/* Hero Section - igual a home.html */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">Bienvenido a TiendaOnline</h1>
          <p className="text-xl mb-8">Encuentra todo lo que necesitas en un solo lugar</p>
          <button
            type="button"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            onClick={() => {
              const el = document.getElementById('productos-destacados');
              if (el) el.scrollIntoView({ behavior: 'smooth' });
            }}
          >
            Ver Productos
          </button>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Nuestras Categorías</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {categorias.map((categoria) => (
              <div
                key={categoria.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
                onClick={() => navigate(`/categorias/${categoria.id}/productos`)}
              >
                {categoria.imagen ? (
                  <img
                    src={categoria.imagen}
                    alt={categoria.nombre}
                    className="w-full h-48 object-cover"
                  />
                ) : (
                  <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
                    <i className="fas fa-box text-white text-4xl" />
                  </div>
                )}
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{categoria.nombre}</h3>
                  <p className="text-gray-600 mb-4">
                    {categoria.descripcion || 'Explora nuestra selección de productos'}
                  </p>
                  <span className="text-blue-600 font-semibold hover:underline">
                    Ver productos <i className="fas fa-arrow-right ml-1" />
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section id="productos-destacados" className="py-16 bg-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Productos Destacados</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {productos.map((producto) => (
              <div
                key={producto.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
              >
                {producto.imagen ? (
                  <img
                    src={producto.imagen}
                    alt={producto.nombre}
                    className="w-full h-48 object-cover"
                  />
                ) : (
                  <div className="w-full h-48 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                    <i className="fas fa-image text-gray-400 text-3xl" />
                  </div>
                )}
                <div className="p-6 flex flex-col h-full">
                  <h3 className="text-lg font-semibold mb-2">{producto.nombre}</h3>
                  <p className="text-gray-600 text-sm mb-3">
                    {producto.descripcion?.length > 90
                      ? `${producto.descripcion.slice(0, 90)}...`
                      : producto.descripcion}
                  </p>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-2xl font-bold text-blue-600">${producto.precio}</span>
                    <span className="text-sm text-gray-500">Stock: {producto.stock}</span>
                  </div>
                  <div className="flex flex-col space-y-2 mt-auto">
                    <button
                      type="button"
                      className="w-full bg-blue-600 text-white text-center py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                      onClick={() => navigate(`/producto/${producto.id}`)}
                    >
                      Ver Detalle
                    </button>
                    <button
                      type="button"
                      className="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition-colors text-sm font-semibold"
                      onClick={() => addToCart.mutate({ productoId: producto.id, cantidad: 1 })}
                    >
                      AGREGAR AL CARRITO
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
