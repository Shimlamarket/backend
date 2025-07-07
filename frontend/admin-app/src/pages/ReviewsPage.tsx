import React, { useState } from 'react'

// Placeholder review data
const reviews = [
  { id: 1, shop: 'Pizza Palace', product: 'Fresh Red Apples', user: 'Alice', rating: 5, comment: 'Great!', date: '2024-06-01', status: 'pending' },
  { id: 2, shop: 'Burger House', product: 'Veggie Burger', user: 'Bob', rating: 2, comment: 'Not good.', date: '2024-06-02', status: 'flagged' },
  { id: 3, shop: 'Pizza Palace', product: 'Fresh Red Apples', user: 'Charlie', rating: 4, comment: 'Tasty.', date: '2024-06-03', status: 'approved' },
]

const unique = (arr: any[], key: string) => Array.from(new Set(arr.map(r => r[key]))).filter(Boolean)

const ReviewsPage: React.FC = () => {
  const [filterShop, setFilterShop] = useState('all')
  const [filterProduct, setFilterProduct] = useState('all')
  const [filterUser, setFilterUser] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [sort, setSort] = useState('newest')

  let filtered = reviews
  if (filterShop !== 'all') filtered = filtered.filter(r => r.shop === filterShop)
  if (filterProduct !== 'all') filtered = filtered.filter(r => r.product === filterProduct)
  if (filterUser !== 'all') filtered = filtered.filter(r => r.user === filterUser)
  if (filterStatus !== 'all') filtered = filtered.filter(r => r.status === filterStatus)
  switch (sort) {
    case 'newest':
      filtered = [...filtered].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      break
    case 'oldest':
      filtered = [...filtered].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
      break
    case 'highest':
      filtered = [...filtered].sort((a, b) => b.rating - a.rating)
      break
    case 'lowest':
      filtered = [...filtered].sort((a, b) => a.rating - b.rating)
      break
    default:
      break
  }

  const handleAction = (id: number, action: string) => {
    // Placeholder: Implement approve/reject/flag logic
    alert(`Review ${id} ${action}`)
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Review Moderation</h2>
      <div className="flex gap-4 mb-4">
        <select className="input-field" value={filterShop} onChange={e => setFilterShop(e.target.value)}>
          <option value="all">All Shops</option>
          {unique(reviews, 'shop').map(shop => <option key={shop} value={shop}>{shop}</option>)}
        </select>
        <select className="input-field" value={filterProduct} onChange={e => setFilterProduct(e.target.value)}>
          <option value="all">All Products</option>
          {unique(reviews, 'product').map(product => <option key={product} value={product}>{product}</option>)}
        </select>
        <select className="input-field" value={filterUser} onChange={e => setFilterUser(e.target.value)}>
          <option value="all">All Users</option>
          {unique(reviews, 'user').map(user => <option key={user} value={user}>{user}</option>)}
        </select>
        <select className="input-field" value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
          <option value="all">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="flagged">Flagged</option>
        </select>
        <select className="input-field" value={sort} onChange={e => setSort(e.target.value)}>
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
          <option value="highest">Highest Rating</option>
          <option value="lowest">Lowest Rating</option>
        </select>
      </div>
      <ul className="space-y-4">
        {filtered.map(r => (
          <li key={r.id} className="card p-4 flex flex-col gap-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-bold text-primary-600">{r.shop}</span>
              <span className="font-bold">{r.product}</span>
              <span className="text-yellow-500">{'★'.repeat(r.rating)}</span>
              <span className="text-xs text-gray-400">{r.date}</span>
              <span className="text-xs text-gray-500">by {r.user}</span>
              <span className="text-xs px-2 py-1 rounded bg-gray-100 ml-2">{r.status}</span>
            </div>
            <div className="text-gray-700 mb-1">{r.comment}</div>
            <div className="flex gap-2 mt-2">
              <button className="btn-primary btn-xs" onClick={() => handleAction(r.id, 'approve')}>Approve</button>
              <button className="btn-secondary btn-xs" onClick={() => handleAction(r.id, 'reject')}>Reject</button>
              <button className="btn-secondary btn-xs" onClick={() => handleAction(r.id, 'flag')}>Flag</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ReviewsPage 