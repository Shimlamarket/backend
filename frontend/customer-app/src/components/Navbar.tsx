import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import {
  ShoppingCartIcon,
  UserIcon,
  Bars3Icon,
  XMarkIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore()
  const navigate = useNavigate()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/shops?search=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  return (
    <nav className="sticky top-0 z-30 bg-white/90 backdrop-blur shadow-nav border-b border-primary-100">
      <div className="container mx-auto px-4 flex justify-between items-center h-20">
        {/* Logo */}
        <Link to="/" className="flex items-center space-x-2">
          <div className="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center shadow">
            <span className="text-white font-bold text-2xl tracking-tight">S</span>
          </div>
          <span className="text-2xl font-extrabold text-primary-600 tracking-tight">ShopHub</span>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-lg mx-8">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Search for shops, products, or cuisines..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-field pl-12 pr-4 py-3 text-lg bg-gray-50"
            />
            <MagnifyingGlassIcon className="absolute left-4 top-3 h-6 w-6 text-primary-400" />
          </div>
        </form>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-8">
          <Link to="/shops" className="text-gray-700 hover:text-primary-500 font-semibold transition-colors">Shops</Link>
          {isAuthenticated ? (
            <>
              <Link to="/cart" className="relative text-gray-700 hover:text-primary-500 transition-colors">
                <ShoppingCartIcon className="h-7 w-7" />
                <span className="absolute -top-2 -right-2 bg-primary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center shadow">0</span>
              </Link>
              <div className="relative group">
                <button className="flex items-center space-x-2 text-gray-700 hover:text-primary-500 font-semibold transition-colors">
                  <UserIcon className="h-7 w-7" />
                  <span>{user?.name}</span>
                </button>
                <div className="absolute right-0 mt-2 w-52 bg-white rounded-xl shadow-card border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <Link to="/profile" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl">Profile</Link>
                  <Link to="/orders" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl">Orders</Link>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl"
                  >Logout</button>
                </div>
              </div>
            </>
          ) : (
            <Link to="/login" className="btn-primary">Login</Link>
          )}
        </div>

        {/* Mobile menu button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="md:hidden p-2 rounded-xl text-primary-600 hover:bg-primary-50"
        >
          {isMenuOpen ? (
            <XMarkIcon className="h-7 w-7" />
          ) : (
            <Bars3Icon className="h-7 w-7" />
          )}
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden py-4 border-t border-primary-100 bg-white/95 backdrop-blur-xl">
          <form onSubmit={handleSearch} className="mb-4 px-4">
            <div className="relative">
              <input
                type="text"
                placeholder="Search for shops, products, or cuisines..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input-field pl-12 pr-4 py-3 text-lg bg-gray-50"
              />
              <MagnifyingGlassIcon className="absolute left-4 top-3 h-6 w-6 text-primary-400" />
            </div>
          </form>
          <div className="space-y-2 px-4">
            <Link to="/shops" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl" onClick={() => setIsMenuOpen(false)}>Shops</Link>
            {isAuthenticated ? (
              <>
                <Link to="/cart" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl" onClick={() => setIsMenuOpen(false)}>Cart</Link>
                <Link to="/profile" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl" onClick={() => setIsMenuOpen(false)}>Profile</Link>
                <Link to="/orders" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl" onClick={() => setIsMenuOpen(false)}>Orders</Link>
                <button
                  onClick={() => {
                    handleLogout()
                    setIsMenuOpen(false)
                  }}
                  className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl"
                >Logout</button>
              </>
            ) : (
              <Link to="/login" className="block px-4 py-3 text-gray-700 hover:bg-primary-50 rounded-xl" onClick={() => setIsMenuOpen(false)}>Login</Link>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar 