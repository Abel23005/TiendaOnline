import { useParams } from 'react-router-dom';
import { useProductsByCategory, useAddToCart } from '../api/hooks';

export default function ProductsByCategory() {
  const { id } = useParams();
  const { data, isLoading } = useProductsByCategory(id);
  const addToCart = useAddToCart();

  if (isLoading) return <div>Cargando productos...</div>;

  const productos = data?.productos || [];
  const categoria = data?.categoria;

  return (
    <div>
      <div className="hero-wrapper">
        <section className="hero">
          <h1 className="hero-title">{categoria?.nombre}</h1>
          <p className="hero-subtitle">Productos disponibles en esta categoría.</p>
        </section>
      </div>

      <h2 className="section-title">Productos de {categoria?.nombre}</h2>
      <ul>
        {productos.map((p) => (
          <li key={p.id}>
            {p.nombre} - ${p.precio}
            <button
              onClick={() => addToCart.mutate({ productoId: p.id, cantidad: 1 })}
              style={{ marginLeft: 8 }}
            >
              Agregar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
