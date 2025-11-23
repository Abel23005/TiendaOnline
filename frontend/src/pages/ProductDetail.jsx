import { useParams } from 'react-router-dom';
import { useProduct, useAddToCart } from '../api/hooks';

export default function ProductDetail() {
  const { id } = useParams();
  const { data, isLoading } = useProduct(id);
  const addToCart = useAddToCart();

  if (isLoading) return <div>Cargando producto...</div>;

  const p = data;
  if (!p) return <div>Producto no encontrado</div>;

  return (
    <div>
      <div className="hero-wrapper">
        <section className="hero">
          <h1 className="hero-title">{p.nombre}</h1>
          <p className="hero-subtitle">{p.descripcion}</p>
        </section>
      </div>

      <div className="card" style={{ maxWidth: '640px', margin: '0 auto' }}>
        <div className="card-price" style={{ marginBottom: '1rem' }}>Precio: ${p.precio}</div>
        <button
          type="button"
          className="btn"
          onClick={() => addToCart.mutate({ productoId: p.id, cantidad: 1 })}
        >
          Agregar al carrito
        </button>
      </div>
    </div>
  );
}
