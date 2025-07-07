import React from 'react'

// Placeholder cart data
const cartItems = [
  {
    id: 'prod1',
    name: 'Fresh Red Apples',
    price: 120,
    quantity: 2,
    image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300&h=200&fit=crop',
    offer: { name: '20% Off on Fruits', discount: 24 },
  },
  {
    id: 'prod2',
    name: 'Organic Whole Milk',
    price: 60,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=200&fit=crop',
    offer: null,
  },
]

const CartPage: React.FC = () => {
  const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const totalDiscount = cartItems.reduce((sum, item) => sum + (item.offer ? item.offer.discount * item.quantity : 0), 0)
  const total = subtotal - totalDiscount

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Your Cart</h2>
      {cartItems.length === 0 ? (
        <div className="text-gray-500">Your cart is empty.</div>
      ) : (
        <div className="space-y-6">
          <ul className="divide-y divide-gray-200 mb-6">
            {cartItems.map(item => (
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
              </li>
            ))}
          </ul>
          <div className="bg-gray-50 rounded-xl p-6 shadow-card max-w-md ml-auto">
            <div className="flex justify-between mb-2">
              <span>Subtotal</span>
              <span>₹{subtotal}</span>
            </div>
            <div className="flex justify-between mb-2 text-green-600">
              <span>Discount</span>
              <span>-₹{totalDiscount}</span>
            </div>
            <div className="flex justify-between font-bold text-lg mt-4">
              <span>Total</span>
              <span>₹{total}</span>
            </div>
            <button className="btn-primary w-full mt-6">Proceed to Checkout</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default CartPage 