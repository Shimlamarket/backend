import React from 'react'
import { useParams, Link } from 'react-router-dom'

const menu = [
  { id: 1, name: 'Margherita Pizza', price: 299, img: 'https://source.unsplash.com/400x200/?pizza' },
  { id: 2, name: 'Veggie Burger', price: 199, img: 'https://source.unsplash.com/400x200/?burger' },
  { id: 3, name: 'Chocolate Cake', price: 149, img: 'https://source.unsplash.com/400x200/?cake' },
]

const ShopDetailPage: React.FC = () => {
  const { shopId } = useParams()
  return (
    <div>
      {/* Banner */}
      <div className="rounded-xl overflow-hidden mb-8">
        <img src={`https://source.unsplash.com/1200x350/?restaurant,food,${shopId}`} alt="Shop Banner" className="w-full h-48 md:h-72 object-cover" />
      </div>
      {/* Info Panel */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
        <div>
          <h2 className="text-3xl font-extrabold text-primary-600 mb-1">Shop Name {shopId}</h2>
          <p className="text-gray-500 mb-2">Pizza, Italian • 4.5★ • 30-40 min</p>
          <span className="inline-block bg-primary-100 text-primary-600 px-3 py-1 rounded-xl text-sm font-semibold">Open Now</span>
        </div>
        <div className="flex gap-4">
          <button className="btn-secondary">Call</button>
          <button className="btn-primary">Directions</button>
        </div>
      </div>
      {/* Menu Grid */}
      <h3 className="text-2xl font-bold mb-4">Menu</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-12">
        {menu.map((item) => (
          <div key={item.id} className="card flex flex-col items-center">
            <img src={item.img} alt={item.name} className="rounded-xl w-full h-32 object-cover mb-4" />
            <h4 className="text-lg font-bold mb-1">{item.name}</h4>
            <p className="text-primary-600 font-semibold mb-2">₹{item.price}</p>
            <button className="btn-primary w-full">Add to Cart</button>
          </div>
        ))}
      </div>
      {/* Reviews Tab (placeholder) */}
      <div className="card">
        <h4 className="text-xl font-bold mb-2">Reviews</h4>
        <p className="text-gray-500">Customer reviews will appear here. (Coming soon!)</p>
      </div>
    </div>
  )
}

export default ShopDetailPage 