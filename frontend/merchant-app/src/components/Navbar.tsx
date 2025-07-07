import React from 'react'
import { Link } from 'react-router-dom'

const Navbar: React.FC = () => (
  <nav className="bg-white shadow-sm border-b border-gray-200">
    <div className="container mx-auto px-4 flex justify-between items-center h-16">
      <Link to="/" className="flex items-center space-x-2">
        <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-lg">M</span>
        </div>
        <span className="text-xl font-bold text-gray-900">Merchant</span>
      </Link>
      <div className="flex items-center space-x-6">
        <Link to="/shops" className="text-gray-700 hover:text-primary-600 transition-colors">Shops</Link>
        <Link to="/products" className="text-gray-700 hover:text-primary-600 transition-colors">Products</Link>
        <Link to="/orders" className="text-gray-700 hover:text-primary-600 transition-colors">Orders</Link>
        <Link to="/profile" className="text-gray-700 hover:text-primary-600 transition-colors">Profile</Link>
      </div>
    </div>
  </nav>
)

export default Navbar 