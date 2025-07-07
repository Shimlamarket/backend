import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import DashboardPage from './pages/DashboardPage'
import ShopApprovalPage from './pages/ShopApprovalPage'
import ShopsPage from './pages/ShopsPage'
import UsersPage from './pages/UsersPage'
import OrdersPage from './pages/OrdersPage'
import ReviewsPage from './pages/ReviewsPage'
import SettingsPage from './pages/SettingsPage'
import ProfilePage from './pages/ProfilePage'
import LoginPage from './pages/LoginPage'
import ProtectedRoute from './components/ProtectedRoute'

const App: React.FC = () => (
  <div className="min-h-screen bg-gray-50">
    <Navbar />
    <main className="container mx-auto px-4 py-8">
      <Routes>
        <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/shop-approvals" element={<ProtectedRoute><ShopApprovalPage /></ProtectedRoute>} />
        <Route path="/shops" element={<ProtectedRoute><ShopsPage /></ProtectedRoute>} />
        <Route path="/users" element={<ProtectedRoute><UsersPage /></ProtectedRoute>} />
        <Route path="/orders" element={<ProtectedRoute><OrdersPage /></ProtectedRoute>} />
        <Route path="/reviews" element={<ProtectedRoute><ReviewsPage /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </main>
  </div>
)

export default App 