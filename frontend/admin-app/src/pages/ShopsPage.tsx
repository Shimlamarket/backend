import React, { useState } from 'react'

// Placeholder offer data
const offers = [
  { id: 1, shop: 'Pizza Palace', name: '10% Off Entire Shop', type: 'percentage', value: 10, status: 'active', valid_from: '2024-06-01', valid_till: '2024-06-30' },
  { id: 2, shop: 'Burger House', name: 'Buy 2 Get 1 Free', type: 'bogo', value: null, status: 'inactive', valid_from: '2024-06-01', valid_till: '2024-06-15' },
  { id: 3, shop: 'Pizza Palace', name: '20% Off on Fruits', type: 'percentage', value: 20, status: 'pending', valid_from: '2024-06-10', valid_till: '2024-06-20' },
]

const unique = (arr: any[], key: string) => Array.from(new Set(arr.map(r => r[key]))).filter(Boolean)

const ShopsPage: React.FC = () => {
  const [filterShop, setFilterShop] = useState('all')
  const [filterType, setFilterType] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')

  let filtered = offers
  if (filterShop !== 'all') filtered = filtered.filter(o => o.shop === filterShop)
  if (filterType !== 'all') filtered = filtered.filter(o => o.type === filterType)
  if (filterStatus !== 'all') filtered = filtered.filter(o => o.status === filterStatus)

  const handleAction = (id: number, action: string) => {
    // Placeholder: Implement approve/deactivate logic
    alert(`Offer ${id} ${action}`)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Offer Management</h2>
      <div className="flex gap-4 mb-4">
        <select className="input-field" value={filterShop} onChange={e => setFilterShop(e.target.value)}>
          <option value="all">All Shops</option>
          {unique(offers, 'shop').map(shop => <option key={shop} value={shop}>{shop}</option>)}
        </select>
        <select className="input-field" value={filterType} onChange={e => setFilterType(e.target.value)}>
          <option value="all">All Types</option>
          {unique(offers, 'type').map(type => <option key={type} value={type}>{type}</option>)}
        </select>
        <select className="input-field" value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
          <option value="all">All Statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="pending">Pending</option>
        </select>
      </div>
      <ul className="space-y-4">
        {filtered.map(o => (
          <li key={o.id} className="card p-4 flex flex-col gap-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-bold text-primary-600">{o.shop}</span>
              <span className="font-bold">{o.name}</span>
              <span className="text-xs text-gray-500">({o.type === 'percentage' ? `${o.value}%` : o.type})</span>
              <span className="text-xs text-gray-400">{o.valid_from} - {o.valid_till}</span>
              <span className="text-xs px-2 py-1 rounded bg-gray-100 ml-2">{o.status}</span>
            </div>
            <div className="flex gap-2 mt-2">
              <button className="btn-primary btn-xs" onClick={() => handleAction(o.id, 'approve')}>Approve</button>
              <button className="btn-secondary btn-xs" onClick={() => handleAction(o.id, 'deactivate')}>Deactivate</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ShopsPage 