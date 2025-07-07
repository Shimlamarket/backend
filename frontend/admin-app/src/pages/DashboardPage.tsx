import React from 'react'

const stats = {
  totalShops: 12,
  totalProducts: 48,
  totalOffers: 7,
  totalReviews: 32,
  avgRating: 4.2,
}

const topShops = [
  { name: 'Pizza Palace', orders: 120, rating: 4.7 },
  { name: 'Burger House', orders: 98, rating: 4.5 },
]

const topProducts = [
  { name: 'Fresh Red Apples', orders: 60 },
  { name: 'Veggie Burger', orders: 45 },
]

const topOffers = [
  { name: '20% Off on Fruits', redemptions: 35 },
  { name: '10% Off Entire Shop', redemptions: 28 },
]

const reviewTrends = [
  { date: '2024-06-01', count: 3 },
  { date: '2024-06-02', count: 5 },
  { date: '2024-06-03', count: 2 },
]

const DashboardPage: React.FC = () => (
  <div>
    <h2 className="text-2xl font-bold mb-4">Admin Analytics Dashboard</h2>
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div className="bg-white rounded-xl shadow-card p-4 text-center">
        <div className="text-3xl font-bold text-primary-600">{stats.totalShops}</div>
        <div className="text-gray-500">Shops</div>
      </div>
      <div className="bg-white rounded-xl shadow-card p-4 text-center">
        <div className="text-3xl font-bold text-primary-600">{stats.totalProducts}</div>
        <div className="text-gray-500">Products</div>
      </div>
      <div className="bg-white rounded-xl shadow-card p-4 text-center">
        <div className="text-3xl font-bold text-primary-600">{stats.totalOffers}</div>
        <div className="text-gray-500">Offers</div>
      </div>
      <div className="bg-white rounded-xl shadow-card p-4 text-center">
        <div className="text-3xl font-bold text-primary-600">{stats.totalReviews}</div>
        <div className="text-gray-500">Reviews</div>
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <div className="bg-white rounded-xl shadow-card p-6">
        <h3 className="font-bold mb-2">Top Shops</h3>
        <ul>
          {topShops.map(s => (
            <li key={s.name} className="flex justify-between mb-1">
              <span>{s.name}</span>
              <span>{s.orders} orders • ★ {s.rating}</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="bg-white rounded-xl shadow-card p-6">
        <h3 className="font-bold mb-2">Top Products</h3>
        <ul>
          {topProducts.map(p => (
            <li key={p.name} className="flex justify-between mb-1">
              <span>{p.name}</span>
              <span>{p.orders} orders</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <div className="bg-white rounded-xl shadow-card p-6">
        <h3 className="font-bold mb-2">Most Used Offers</h3>
        <ul>
          {topOffers.map(o => (
            <li key={o.name} className="flex justify-between mb-1">
              <span>{o.name}</span>
              <span>{o.redemptions} redemptions</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="bg-white rounded-xl shadow-card p-6">
        <h3 className="font-bold mb-2">Review Trends</h3>
        <ul>
          {reviewTrends.map(r => (
            <li key={r.date} className="flex justify-between mb-1">
              <span>{r.date}</span>
              <span>{r.count} reviews</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
    <div className="bg-white rounded-xl shadow-card p-6 max-w-xs">
      <div className="font-bold mb-2">Average Rating</div>
      <div className="text-2xl text-yellow-500 font-bold">★ {stats.avgRating}</div>
    </div>
  </div>
)

export default DashboardPage 