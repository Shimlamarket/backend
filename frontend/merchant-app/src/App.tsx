import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import DashboardPage from './pages/DashboardPage'
import ShopsPage from './pages/ShopsPage'
import ShopDetailPage from './pages/ShopDetailPage'
import ProductsPage from './pages/ProductsPage'
import OrdersPage from './pages/OrdersPage'
import ProfilePage from './pages/ProfilePage'
import LoginPage from './pages/LoginPage'
import ProtectedRoute from './components/ProtectedRoute'

const App: React.FC = () => (
  <div className="min-h-screen bg-gray-50">
    <Navbar />
    <main className="container mx-auto px-4 py-8">
      <Routes>
        <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/shops" element={<ProtectedRoute><ShopsPage /></ProtectedRoute>} />
        <Route path="/shops/:shopId" element={<ProtectedRoute><ShopDetailPage /></ProtectedRoute>} />
        <Route path="/products" element={<ProtectedRoute><ProductsPage /></ProtectedRoute>} />
        <Route path="/orders" element={<ProtectedRoute><OrdersPage /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </main>
  </div>
)

export default App 