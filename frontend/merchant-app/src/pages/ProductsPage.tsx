import React, { useState } from 'react'

// Placeholder product and offer data
const products = [
  {
    id: 'prod1',
    name: 'Fresh Red Apples',
    offers: [
      { offer_id: 'off1', name: '20% Off on Fruits', type: 'percentage', value: 20, active: true, valid_from: '2024-06-01', valid_till: '2024-06-30' },
    ],
  },
  {
    id: 'prod2',
    name: 'Organic Whole Milk',
    offers: [],
  },
]

const ProductsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false)
  const [editOffer, setEditOffer] = useState<any>(null)
  const [currentProduct, setCurrentProduct] = useState<any>(null)

  const handleCreate = (product: any) => {
    setEditOffer(null)
    setCurrentProduct(product)
    setShowModal(true)
  }
  const handleEdit = (product: any, offer: any) => {
    setEditOffer(offer)
    setCurrentProduct(product)
    setShowModal(true)
  }
  const handleClose = () => setShowModal(false)

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Your Products</h2>
      <div className="space-y-8">
        {products.map(product => (
          <div key={product.id} className="bg-white rounded-xl shadow-card p-6">
            <div className="flex items-center justify-between mb-2">
              <div className="font-bold text-lg">{product.name}</div>
              <button className="btn-primary" onClick={() => handleCreate(product)}>Create Offer</button>
            </div>
            <ul className="ml-4 list-disc text-green-700">
              {product.offers.length === 0 ? (
                <li className="text-gray-400">No offers for this product.</li>
              ) : (
                product.offers.map(offer => (
                  <li key={offer.offer_id} className="font-semibold flex items-center gap-2">
                    Offer: {offer.name} <span className="text-xs text-gray-500">({offer.type === 'percentage' ? `${offer.value}%` : `₹${offer.value}`} | {offer.active ? 'Active' : 'Inactive'})</span>
                    <span className="text-xs text-gray-400">{offer.valid_from} - {offer.valid_till}</span>
                    <button className="btn-secondary text-xs" onClick={() => handleEdit(product, offer)}>Edit</button>
                  </li>
                ))
              )}
            </ul>
          </div>
        ))}
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-card p-8 w-full max-w-md relative">
            <button className="absolute top-2 right-2 text-gray-400 hover:text-gray-700" onClick={handleClose}>×</button>
            <h3 className="text-xl font-bold mb-4">{editOffer ? 'Edit Offer' : `Create Offer for ${currentProduct?.name}`}</h3>
            <form className="space-y-4">
              <div>
                <label className="block font-semibold mb-1">Offer Name</label>
                <input className="input-field w-full" defaultValue={editOffer?.name || ''} required />
              </div>
              <div>
                <label className="block font-semibold mb-1">Type</label>
                <select className="input-field w-full" defaultValue={editOffer?.type || 'percentage'} required>
                  <option value="percentage">Percentage</option>
                  <option value="fixed">Fixed Amount</option>
                </select>
              </div>
              <div>
                <label className="block font-semibold mb-1">Value</label>
                <input className="input-field w-full" type="number" defaultValue={editOffer?.value || ''} required />
              </div>
              <div className="flex gap-2">
                <div className="flex-1">
                  <label className="block font-semibold mb-1">Valid From</label>
                  <input className="input-field w-full" type="date" defaultValue={editOffer?.valid_from || ''} required />
                </div>
                <div className="flex-1">
                  <label className="block font-semibold mb-1">Valid Till</label>
                  <input className="input-field w-full" type="date" defaultValue={editOffer?.valid_till || ''} required />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <input type="checkbox" defaultChecked={editOffer?.active ?? true} id="active" />
                <label htmlFor="active" className="font-semibold">Active</label>
              </div>
              <button className="btn-primary w-full mt-2" type="submit">{editOffer ? 'Update Offer' : 'Create Offer'}</button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductsPage 