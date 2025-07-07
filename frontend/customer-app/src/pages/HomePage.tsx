import React from 'react'
import { Link } from 'react-router-dom'

const categories = [
  { name: 'Pizza', icon: '🍕' },
  { name: 'Burgers', icon: '🍔' },
  { name: 'Desserts', icon: '🍰' },
  { name: 'Chinese', icon: '🥡' },
  { name: 'Drinks', icon: '🥤' },
  { name: 'Healthy', icon: '🥗' },
]

const HomePage: React.FC = () => (
  <div>
    {/* Hero Section */}
    <section className="bg-primary-500 rounded-xl shadow-card p-8 md:p-16 flex flex-col items-center text-center mb-10">
      <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">Discover the Best Food & Shops Near You</h1>
      <p className="text-lg md:text-2xl text-primary-100 mb-8">Order from your favorite local restaurants and shops, fast and easy.</p>
      <form className="w-full max-w-xl mx-auto flex bg-white rounded-xl shadow overflow-hidden">
        <input
          type="text"
          placeholder="Search for restaurants, cuisines, or a dish..."
          className="flex-1 px-6 py-4 text-lg focus:outline-none"
        />
        <button type="submit" className="btn-primary rounded-none rounded-r-xl text-lg">Search</button>
      </form>
    </section>

    {/* Categories */}
    <section className="mb-12">
      <h2 className="section-title">Popular Categories</h2>
      <div className="grid grid-cols-3 sm:grid-cols-6 gap-4 justify-items-center">
        {categories.map((cat) => (
          <Link key={cat.name} to={`/shops?category=${cat.name.toLowerCase()}`} className="flex flex-col items-center bg-white rounded-xl shadow-card p-4 hover:bg-primary-50 transition">
            <span className="text-3xl mb-2">{cat.icon}</span>
            <span className="font-semibold text-primary-600">{cat.name}</span>
          </Link>
        ))}
      </div>
    </section>

    {/* Featured Shops (placeholder) */}
    <section className="mb-12">
      <h2 className="section-title">Featured Shops</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {[1,2,3].map((i) => (
          <div key={i} className="card flex flex-col items-center">
            <img src={`https://source.unsplash.com/400x200/?food,restaurant,${i}`} alt="Shop" className="rounded-xl w-full h-32 object-cover mb-4" />
            <h3 className="text-xl font-bold mb-1">Shop Name {i}</h3>
            <p className="text-gray-500 mb-2">Category • 4.{i}★ • 30-40 min</p>
            <Link to="/shops/1" className="btn-secondary w-full">View Shop</Link>
          </div>
        ))}
      </div>
    </section>

    {/* How it works */}
    <section className="mb-12">
      <h2 className="section-title">How it Works</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="card flex flex-col items-center">
          <span className="text-4xl mb-2">🔍</span>
          <h4 className="font-bold mb-1">Browse & Search</h4>
          <p className="text-gray-500">Find shops, products, and cuisines you love.</p>
        </div>
        <div className="card flex flex-col items-center">
          <span className="text-4xl mb-2">🛒</span>
          <h4 className="font-bold mb-1">Add to Cart</h4>
          <p className="text-gray-500">Add your favorite items to the cart and checkout.</p>
        </div>
        <div className="card flex flex-col items-center">
          <span className="text-4xl mb-2">🚚</span>
          <h4 className="font-bold mb-1">Fast Delivery</h4>
          <p className="text-gray-500">Get your order delivered quickly to your doorstep.</p>
        </div>
      </div>
    </section>
  </div>
)

export default HomePage 