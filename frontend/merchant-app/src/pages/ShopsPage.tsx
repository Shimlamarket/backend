import React, { useState } from 'react'

const shopOffers = [
  { offer_id: 'off1', name: '10% Off Entire Shop', type: 'percentage', value: 10, active: true, valid_from: '2024-06-01', valid_till: '2024-06-30' },
]

const ShopsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false)
  const [editOffer, setEditOffer] = useState<any>(null)

  const handleCreate = () => {
    setEditOffer(null)
    setShowModal(true)
  }
  const handleEdit = (offer: any) => {
    setEditOffer(offer)
    setShowModal(true)
  }
  const handleClose = () => setShowModal(false)

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Your Shops</h2>
      <div className="mb-6">
        <ul className="mb-2">
          {shopOffers.map(offer => (
            <li key={offer.offer_id} className="flex items-center gap-2 mb-1">
              <span className="font-semibold text-green-700">{offer.name}</span>
              <span className="text-xs text-gray-500">({offer.type === 'percentage' ? `${offer.value}%` : `₹${offer.value}`} | {offer.active ? 'Active' : 'Inactive'})</span>
              <span className="text-xs text-gray-400">{offer.valid_from} - {offer.valid_till}</span>
              <button className="btn-secondary text-xs" onClick={() => handleEdit(offer)}>Edit</button>
            </li>
          ))}
        </ul>
        <button className="btn-primary" onClick={handleCreate}>Create Shop Offer</button>
      </div>
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-card p-8 w-full max-w-md relative">
            <button className="absolute top-2 right-2 text-gray-400 hover:text-gray-700" onClick={handleClose}>×</button>
            <h3 className="text-xl font-bold mb-4">{editOffer ? 'Edit Offer' : 'Create Shop Offer'}</h3>
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

export default ShopsPage 