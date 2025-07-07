import React from 'react'
import { Navigate } from 'react-router-dom'

const isAuthenticated = true // TODO: Replace with real auth logic

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

export default ProtectedRoute 