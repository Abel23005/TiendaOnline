import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Cart from './pages/Cart'
import Categories from './pages/Categories'
import ProductsByCategory from './pages/ProductsByCategory'
import ProductDetail from './pages/ProductDetail'
import { useCart } from './api/hooks'
import './App.css'

function App() {
  const { data } = useCart()
  const cartCount = data?.total_items ?? 0

  return (
    <div>
      <header>
        <div className="header-inner">
          <div className="brand">
            <div className="brand-icon">T</div>
            <span>TiendaOnline</span>
          </div>

          <div className="header-center">
            <input
              type="text"
              className="search-input"
              placeholder="Buscar productos..."
            />
          </div>

          <div className="header-right">
            <nav>
              <Link to="/">Inicio</Link>
              <Link to="/categorias">Categorías</Link>
            </nav>
            <button
              type="button"
              className="cart-pill"
              onClick={() => {
                window.location.href = '/carrito'
              }}
            >
              <span className="cart-icon">🛒</span>
              <span className="cart-count">{cartCount}</span>
            </button>
          </div>
        </div>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/carrito" element={<Cart />} />
          <Route path="/categorias" element={<Categories />} />
          <Route path="/categorias/:id/productos" element={<ProductsByCategory />} />
          <Route path="/producto/:id" element={<ProductDetail />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
