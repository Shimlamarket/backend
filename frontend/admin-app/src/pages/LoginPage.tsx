import React from 'react'

const LoginPage: React.FC = () => (
  <div className="max-w-md mx-auto mt-16 p-8 bg-white rounded-lg shadow-md">
    <h2 className="text-2xl font-bold mb-4 text-center">Admin Login</h2>
    <p className="text-gray-600 mb-6 text-center">Sign in with Google as an admin.</p>
    <button className="btn-primary w-full py-2">Sign in with Google</button>
    <p className="text-xs text-gray-400 mt-4 text-center">(Google OAuth coming soon!)</p>
  </div>
)

export default LoginPage 