import React from 'react'
import { useParams, Link } from 'react-router-dom'

// Placeholder order data
const order = {
  order_id: 'ORD001',
  status: 'Delivered',
  date: '2024-06-01T14:30:00Z',
  total: 300,
  discount: 24,
  items: [
    {
      id: 'prod1',
      name: 'Fresh Red Apples',
      price: 120,
      quantity: 2,
      image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=200&fit=crop',
      offer: { name: '20% Off on Fruits', discount: 24 },
      reviewed: false,
    },
    {
      id: 'prod2',
      name: 'Organic Whole Milk',
      price: 60,
      quantity: 1,
      image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=200&fit=crop',
      offer: null,
      reviewed: true,
    },
  ],
}

const OrderDetailPage: React.FC = () => {
  const { orderId } = useParams()
  // In real app, fetch order by orderId

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Order Details</h2>
      <div className="bg-white rounded-xl shadow-card p-6 mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Order ID:</span>
          <span className="font-mono">{order.order_id}</span>
        </div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Status:</span>
          <span className="font-semibold text-primary-600">{order.status}</span>
        </div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Date:</span>
          <span>{new Date(order.date).toLocaleString()}</span>
        </div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Discount:</span>
          <span className="text-green-600">-₹{order.discount}</span>
        </div>
        <div className="flex justify-between font-bold text-lg mt-4">
          <span>Total Paid:</span>
          <span>₹{order.total - order.discount}</span>
        </div>
      </div>
      <h3 className="text-xl font-bold mb-2">Items</h3>
      <ul className="divide-y divide-gray-200 mb-6">
        {order.items.map(item => (
          <li key={item.id} className="flex items-center gap-4 py-4">
            <img src={item.image} alt={item.name} className="w-20 h-20 rounded-xl object-cover" />
            <div className="flex-1">
              <div className="font-bold text-lg">{item.name}</div>
              <div className="text-gray-500">Qty: {item.quantity}</div>
              {item.offer && (
                <div className="text-green-600 font-semibold text-sm">Offer: {item.offer.name} (-₹{item.offer.discount * item.quantity})</div>
              )}
            </div>
            <div className="font-bold text-primary-600 text-lg">₹{item.price * item.quantity}</div>
            <div>
              {item.reviewed ? (
                <span className="text-green-600 font-semibold text-sm">Reviewed</span>
              ) : (
                <Link to={`/products/${item.id}`} className="btn-secondary text-xs">Leave Review</Link>
              )}
            </div>
          </li>
        ))}
      </ul>
      <Link to="/order-history" className="btn-primary">Back to Orders</Link>
    </div>
  )
}

export default OrderDetailPage 