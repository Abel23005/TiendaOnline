import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { useCategories } from '../api/hooks';

export default function Categories() {
  const { data, isLoading } = useCategories();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  if (isLoading) return <div>Cargando categorías...</div>;

  const categorias = data || [];

  return (
    <div>
      <div className="hero-wrapper">
        <section className="hero">
          <h1 className="hero-title">Explora nuestras categorías</h1>
          <p className="hero-subtitle">Encuentra productos organizados por tipo para llegar más rápido a lo que buscas.</p>
        </section>
      </div>

      <h2 className="section-title">Nuestras Categorías</h2>
      <div className="grid grid-3">
        {categorias.map((c) => (
          <button
            key={c.id}
            type="button"
            className="card"
            onMouseEnter={() => {
              queryClient.prefetchQuery({
                queryKey: ['productosPorCategoria', c.id],
                queryFn: async () => {
                  const res = await fetch(`/api/categorias/${c.id}/productos/`);
                  return res.json();
                },
              });
            }}
            onClick={() => navigate(`/categorias/${c.id}/productos`)}
          >
            {c.imagen && (
              <div style={{ marginBottom: '0.75rem', borderRadius: '0.5rem', overflow: 'hidden' }}>
                <img src={c.imagen} alt={c.nombre} style={{ width: '100%', height: '150px', objectFit: 'cover' }} />
              </div>
            )}
            <div className="card-title">{c.nombre}</div>
            <div className="card-subtitle">{c.descripcion}</div>
            <div className="card-subtitle">{c.productos_count} productos</div>
            <span className="btn btn-secondary">Ver productos</span>
          </button>
        ))}
      </div>
    </div>
  );
}
