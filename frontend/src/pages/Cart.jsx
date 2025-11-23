import { useCart, useUpdateCartItem, useRemoveCartItem } from '../api/hooks';

export default function Cart() {
  const { data, isLoading } = useCart();
  const updateItem = useUpdateCartItem();
  const removeItem = useRemoveCartItem();

  if (isLoading) return <div className="text-center py-10">Cargando carrito...</div>;

  const items = data?.items || [];
  const subtotal = Number(data?.subtotal || 0);
  const shipping = items.length > 0 ? 5 : 0;
  const taxes = subtotal * 0.1;
  const total = subtotal + shipping + taxes;

  const handleChangeQuantity = (item, cantidadNueva) => {
    if (cantidadNueva <= 0) {
      removeItem.mutate(item.id);
    } else {
      updateItem.mutate({ itemId: item.id, cantidad: cantidadNueva });
    }
  };

  const handleClearCart = () => {
    // eliminar cada ítem del carrito mediante la API
    items.forEach((item) => {
      removeItem.mutate(item.id);
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Carrito de Compras</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          {items.length === 0 ? (
            <div className="text-center py-12">
              <i className="fas fa-shopping-cart text-gray-400 text-6xl mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">Tu carrito está vacío</h3>
              <p className="text-gray-500 mb-6">Agrega algunos productos para comenzar</p>
              <a
                href="/"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Continuar Comprando
              </a>
            </div>
          ) : (
            <div className="space-y-4">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md p-6 flex items-center space-x-4"
                >
                  <div className="w-20 h-20 bg-gray-200 rounded-lg overflow-hidden">
                    {item.producto.imagen ? (
                      <img
                        src={item.producto.imagen}
                        alt={item.producto.nombre}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <i className="fas fa-image text-gray-400" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{item.producto.nombre}</h3>
                    <p className="text-gray-600">${item.producto.precio}</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <button
                      type="button"
                      onClick={() => handleChangeQuantity(item, item.cantidad - 1)}
                      className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300 transition-colors"
                    >
                      <i className="fas fa-minus text-sm" />
                    </button>
                    <span className="w-8 text-center font-semibold">{item.cantidad}</span>
                    <button
                      type="button"
                      onClick={() => handleChangeQuantity(item, item.cantidad + 1)}
                      className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300 transition-colors"
                    >
                      <i className="fas fa-plus text-sm" />
                    </button>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-lg">${item.subtotal.toFixed(2)}</p>
                    <button
                      type="button"
                      onClick={() => removeItem.mutate(item.id)}
                      className="text-red-500 hover:text-red-700 transition-colors mt-1"
                    >
                      <i className="fas fa-trash" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="bg-gray-50 rounded-lg p-6 lg:sticky lg:top-24">
            <h3 className="text-lg font-semibold mb-4">Resumen del Pedido</h3>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal:</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Envío:</span>
                <span>${shipping.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Impuestos:</span>
                <span>${taxes.toFixed(2)}</span>
              </div>
              <div className="border-t border-gray-300 pt-3">
                <div className="flex justify-between font-semibold text-lg">
                  <span>Total:</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            <button
              type="button"
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
              disabled={items.length === 0}
            >
              Proceder al Pago
            </button>

            <div className="mt-4 text-center space-y-2">
              <a href="/" className="block text-blue-600 hover:underline">
                <i className="fas fa-arrow-left mr-1" />
                Continuar Comprando
              </a>
              {items.length > 0 && (
                <button
                  type="button"
                  onClick={handleClearCart}
                  className="text-red-500 hover:underline text-sm"
                >
                  <i className="fas fa-trash mr-1" />
                  Limpiar Carrito
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
