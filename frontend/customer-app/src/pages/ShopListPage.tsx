import React from 'react'
import { Link } from 'react-router-dom'

const shops = [
  { id: 1, name: 'Pizza Palace', category: 'Pizza', rating: 4.5, time: '30-40 min', img: 'https://source.unsplash.com/400x200/?pizza,restaurant' },
  { id: 2, name: 'Burger House', category: 'Burgers', rating: 4.2, time: '25-35 min', img: 'https://source.unsplash.com/400x200/?burger,restaurant' },
  { id: 3, name: 'Sweet Treats', category: 'Desserts', rating: 4.8, time: '20-30 min', img: 'https://source.unsplash.com/400x200/?dessert,restaurant' },
]

const ShopListPage: React.FC = () => (
  <div>
    <h2 className="section-title">All Shops</h2>
    {/* Filters (placeholder) */}
    <div className="flex flex-wrap gap-4 mb-8">
      <input type="text" placeholder="Search shops..." className="input-field max-w-xs" />
      <select className="input-field max-w-xs">
        <option>All Categories</option>
        <option>Pizza</option>
        <option>Burgers</option>
        <option>Desserts</option>
      </select>
      <select className="input-field max-w-xs">
        <option>Sort by</option>
        <option>Rating</option>
        <option>Delivery Time</option>
      </select>
    </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {shops.map((shop) => (
        <Link key={shop.id} to={`/shops/${shop.id}`} className="card hover:shadow-lg transition flex flex-col items-center">
          <img src={shop.img} alt={shop.name} className="rounded-xl w-full h-32 object-cover mb-4" />
          <h3 className="text-xl font-bold mb-1">{shop.name}</h3>
          <p className="text-gray-500 mb-2">{shop.category} • {shop.rating}★ • {shop.time}</p>
          <span className="btn-secondary w-full text-center">View Shop</span>
        </Link>
      ))}
    </div>
  </div>
)

export default ShopListPage 