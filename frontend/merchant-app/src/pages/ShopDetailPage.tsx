import React, { useState } from 'react'
import { useParams } from 'react-router-dom'

// Placeholder review data
const reviews = [
  { id: 1, product: 'Fresh Red Apples', rating: 5, comment: 'Great!', date: '2024-06-01' },
  { id: 2, product: 'Organic Whole Milk', rating: 4, comment: 'Good quality.', date: '2024-06-02' },
  { id: 3, product: 'Fresh Red Apples', rating: 3, comment: 'Average.', date: '2024-06-03' },
]

const getAvgRating = (reviews: any[]) => reviews.length ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1) : null

const ShopDetailPage: React.FC = () => {
  const { shopId } = useParams()
  const [sort, setSort] = useState('newest')
  const [filterProduct, setFilterProduct] = useState('all')

  // Unique product names for filter
  const productNames = Array.from(new Set(reviews.map(r => r.product)))

  // Filter and sort reviews
  let filtered = filterProduct === 'all' ? reviews : reviews.filter(r => r.product === filterProduct)
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

  // Review stats
  const avgRating = getAvgRating(reviews)
  const reviewCount = reviews.length
  const productStats = productNames.map(name => ({
    name,
    avg: getAvgRating(reviews.filter(r => r.product === name)),
    count: reviews.filter(r => r.product === name).length,
  }))

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Shop Reviews & Analytics</h2>
      <div className="bg-white rounded-xl shadow-card p-6 mb-6">
        <div className="flex items-center gap-8 mb-4">
          <div>
            <div className="text-lg font-bold text-yellow-500">★ {avgRating || '-'}</div>
            <div className="text-gray-500">{reviewCount} review{reviewCount !== 1 && 's'}</div>
          </div>
          <div>
            <div className="font-semibold mb-1">By Product</div>
            <ul className="text-sm">
              {productStats.map(stat => (
                <li key={stat.name}>{stat.name}: <span className="text-yellow-500">★ {stat.avg || '-'}</span> ({stat.count})</li>
              ))}
            </ul>
          </div>
        </div>
        <div className="flex gap-4 mb-4">
          <select className="input-field" value={filterProduct} onChange={e => setFilterProduct(e.target.value)}>
            <option value="all">All Products</option>
            {productNames.map(name => <option key={name} value={name}>{name}</option>)}
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
                <span className="font-bold text-primary-600">{r.product}</span>
                <span className="text-yellow-500">{'★'.repeat(r.rating)}</span>
                <span className="text-xs text-gray-400">{r.date}</span>
              </div>
              <div className="text-gray-700 mb-1">{r.comment}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ShopDetailPage 