import React from 'react'
import { useParams } from 'react-router-dom'

const OrderDetailPage: React.FC = () => {
  const { orderId } = useParams()
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Order Details</h2>
      <p className="text-gray-600">Details for order <span className="font-mono">{orderId}</span> will appear here. (Coming soon!)</p>
    </div>
  )
}

export default OrderDetailPage 