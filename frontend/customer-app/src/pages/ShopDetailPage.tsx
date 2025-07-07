import React, { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

const API_BASE = 'http://localhost:8001'

const fetchShop = async (shopId: string) => {
  // Placeholder: Replace with real shop fetch if available
  return {
    shop_id: shopId,
    name: `Shop Name ${shopId}`,
    category: 'Pizza',
    rating: 4.5,
    total_reviews: 10,
    banner_url: `https://source.unsplash.com/1200x350/?restaurant,food,${shopId}`,
    is_open: true,
    phone: '1234567890',
    address: '123 Main St',
    offers: [],
  }
}

const fetchOffers = async (shopId: string) => {
  const { data } = await axios.get(`${API_BASE}/offers`, {
    headers: { Authorization: 'Bearer demo-token-123' },
  })
  return data.filter((offer: any) => offer.level === 'merchant' && offer.merchant_id === shopId)
}

const fetchReviews = async (shopId: string) => {
  const { data } = await axios.get(`${API_BASE}/reviews?shop_id=${shopId}`)
  return data
}

const postReview = async (review: any) => {
  const { data } = await axios.post(`${API_BASE}/reviews`, review, {
    headers: { Authorization: 'Bearer demo-token-123' },
  })
  return data
}

const sortReviews = (reviews: any[], sort: string) => {
  switch (sort) {
    case 'newest':
      return [...reviews].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    case 'oldest':
      return [...reviews].sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
    case 'highest':
      return [...reviews].sort((a, b) => b.rating - a.rating)
    case 'lowest':
      return [...reviews].sort((a, b) => a.rating - b.rating)
    default:
      return reviews
  }
}

const menu = [
  { id: 1, name: 'Margherita Pizza', price: 299, img: 'https://source.unsplash.com/400x200/?pizza' },
  { id: 2, name: 'Veggie Burger', price: 199, img: 'https://source.unsplash.com/400x200/?burger' },
  { id: 3, name: 'Chocolate Cake', price: 149, img: 'https://source.unsplash.com/400x200/?cake' },
]

const ShopDetailPage: React.FC = () => {
  const { shopId } = useParams()
  const queryClient = useQueryClient()
  const [reviewForm, setReviewForm] = useState({ rating: 5, title: '', comment: '' })
  const [submitting, setSubmitting] = useState(false)
  const [sort, setSort] = useState('newest')

  // Fetch shop (placeholder)
  const { data: shop } = useQuery(['shop', shopId], () => fetchShop(shopId!), { enabled: !!shopId })
  // Fetch offers
  const { data: offers = [], isLoading: loadingOffers } = useQuery(['shopOffers', shopId], () => fetchOffers(shopId!), { enabled: !!shopId })
  // Fetch reviews
  const { data: reviews = [], isLoading: loadingReviews, error: reviewsError } = useQuery(['shopReviews', shopId], () => fetchReviews(shopId!), { enabled: !!shopId })

  const mutation = useMutation(postReview, {
    onSuccess: () => {
      queryClient.invalidateQueries(['shopReviews', shopId])
      setReviewForm({ rating: 5, title: '', comment: '' })
      setSubmitting(false)
    },
    onError: () => setSubmitting(false),
  })

  const handleReviewSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    mutation.mutate({
      shop_id: shopId,
      rating: reviewForm.rating,
      title: reviewForm.title,
      comment: reviewForm.comment,
      order_id: 'order123',
      customer_id: 'customer123',
    })
  }

  // Calculate average rating and review count
  const avgRating = reviews.length ? (reviews.reduce((sum: number, r: any) => sum + r.rating, 0) / reviews.length).toFixed(1) : null
  const sortedReviews = sortReviews(reviews, sort)

  return (
    <div>
      {/* Banner */}
      <div className="rounded-xl overflow-hidden mb-8">
        <img src={shop?.banner_url} alt="Shop Banner" className="w-full h-48 md:h-72 object-cover" />
      </div>
      {/* Info Panel */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
        <div>
          <h2 className="text-3xl font-extrabold text-primary-600 mb-1">{shop?.name}</h2>
          <p className="text-gray-500 mb-2">{shop?.category} • {shop?.rating}★ • {shop?.is_open ? 'Open Now' : 'Closed'}</p>
          <span className="inline-block bg-primary-100 text-primary-600 px-3 py-1 rounded-xl text-sm font-semibold">{shop?.is_open ? 'Open Now' : 'Closed'}</span>
        </div>
        <div className="flex gap-4">
          <button className="btn-secondary">Call</button>
          <button className="btn-primary">Directions</button>
        </div>
      </div>
      {/* Offers */}
      {loadingOffers ? <div className="animate-pulse">Loading offers...</div> : offers.length > 0 && (
        <div className="mb-8">
          <h4 className="font-bold text-primary-500 mb-2">Shop Offers</h4>
          <ul className="list-disc ml-6">
            {offers.map((offer: any) => (
              <li key={offer.offer_id} className="text-green-700 font-semibold">
                {offer.name}: {offer.description}
              </li>
            ))}
          </ul>
        </div>
      )}
      {/* Menu Grid */}
      <h3 className="text-2xl font-bold mb-4">Menu</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-12">
        {menu.map((item) => (
          <div key={item.id} className="card flex flex-col items-center">
            <img src={item.img} alt={item.name} className="rounded-xl w-full h-32 object-cover mb-4" />
            <h4 className="text-lg font-bold mb-1">{item.name}</h4>
            <p className="text-primary-600 font-semibold mb-2">₹{item.price}</p>
            <button className="btn-primary w-full">Add to Cart</button>
          </div>
        ))}
      </div>
      {/* Reviews */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-2xl font-bold">Customer Reviews</h3>
          <div className="flex items-center gap-4">
            {avgRating && (
              <span className="text-lg font-bold text-yellow-500">★ {avgRating}</span>
            )}
            <span className="text-gray-500">{reviews.length} review{reviews.length !== 1 && 's'}</span>
            <select className="input-field" value={sort} onChange={e => setSort(e.target.value)}>
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
              <option value="highest">Highest Rating</option>
              <option value="lowest">Lowest Rating</option>
            </select>
          </div>
        </div>
        {loadingReviews ? <div className="animate-pulse">Loading reviews...</div> : reviewsError ? <div className="text-red-500">Failed to load reviews.</div> : reviews.length === 0 ? <div>No reviews yet.</div> : (
          <ul className="space-y-4">
            {sortedReviews.map((r: any) => (
              <li key={r.review_id} className="card p-4 flex flex-col gap-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-primary-600">{r.title || 'Review'}</span>
                  <span className="text-yellow-500">{'★'.repeat(r.rating)}</span>
                </div>
                <div className="text-gray-700 mb-1">{r.comment}</div>
                <div className="text-xs text-gray-400">{new Date(r.created_at).toLocaleString()}</div>
              </li>
            ))}
          </ul>
        )}
      </div>
      {/* Add Review */}
      <div className="mb-8">
        <h3 className="text-xl font-bold mb-2">Add Your Review</h3>
        <form onSubmit={handleReviewSubmit} className="space-y-2">
          <div>
            <label className="block font-semibold mb-1">Rating</label>
            <select
              className="input-field"
              value={reviewForm.rating}
              onChange={e => setReviewForm(f => ({ ...f, rating: Number(e.target.value) }))}
              required
            >
              {[5,4,3,2,1].map(n => <option key={n} value={n}>{n} Star{n > 1 && 's'}</option>)}
            </select>
          </div>
          <div>
            <label className="block font-semibold mb-1">Title</label>
            <input
              className="input-field"
              value={reviewForm.title}
              onChange={e => setReviewForm(f => ({ ...f, title: e.target.value }))}
              placeholder="Review title"
              required
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Comment</label>
            <textarea
              className="input-field"
              value={reviewForm.comment}
              onChange={e => setReviewForm(f => ({ ...f, comment: e.target.value }))}
              placeholder="Write your review..."
              required
            />
          </div>
          <button className="btn-primary" type="submit" disabled={submitting}>{submitting ? 'Submitting...' : 'Submit Review'}</button>
        </form>
      </div>
    </div>
  )
}

export default ShopDetailPage 