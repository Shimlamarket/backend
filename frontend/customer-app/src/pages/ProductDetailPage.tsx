import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

const API_BASE = 'http://localhost:8001' // Adjust as needed

const fetchProduct = async (productId: string) => {
  const { data } = await axios.get(`${API_BASE}/products/${productId}`, {
    headers: { Authorization: 'Bearer demo-token-123' },
  })
  return data
}

const fetchOffers = async (offerIds: string[]) => {
  if (!offerIds.length) return []
  const { data } = await axios.get(`${API_BASE}/offers`, {
    headers: { Authorization: 'Bearer demo-token-123' },
  })
  return data.filter((offer: any) => offerIds.includes(offer.offer_id))
}

const fetchReviews = async (productId: string) => {
  const { data } = await axios.get(`${API_BASE}/reviews?product_id=${productId}`)
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

const ProductDetailPage: React.FC = () => {
  const { productId } = useParams()
  const queryClient = useQueryClient()
  const [reviewForm, setReviewForm] = useState({ rating: 5, title: '', comment: '' })
  const [submitting, setSubmitting] = useState(false)
  const [sort, setSort] = useState('newest')

  // Fetch product
  const { data: product, isLoading: loadingProduct, error: productError } = useQuery(['product', productId], () => fetchProduct(productId!), { enabled: !!productId })
  // Fetch offers
  const { data: offers = [], isLoading: loadingOffers } = useQuery(['offers', product?.offers], () => fetchOffers(product?.offers || []), { enabled: !!product?.offers })
  // Fetch reviews
  const { data: reviews = [], isLoading: loadingReviews, error: reviewsError } = useQuery(['reviews', productId], () => fetchReviews(productId!), { enabled: !!productId })

  const mutation = useMutation(postReview, {
    onSuccess: () => {
      queryClient.invalidateQueries(['reviews', productId])
      setReviewForm({ rating: 5, title: '', comment: '' })
      setSubmitting(false)
    },
    onError: () => setSubmitting(false),
  })

  const handleReviewSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    mutation.mutate({
      product_id: productId,
      rating: reviewForm.rating,
      title: reviewForm.title,
      comment: reviewForm.comment,
      order_id: 'order123', // Replace with real order ID in production
      customer_id: 'customer123', // Replace with real customer ID from auth
    })
  }

  // Calculate average rating and review count
  const avgRating = reviews.length ? (reviews.reduce((sum: number, r: any) => sum + r.rating, 0) / reviews.length).toFixed(1) : null
  const sortedReviews = sortReviews(reviews, sort)

  if (loadingProduct) return <div className="animate-pulse">Loading product...</div>
  if (productError) return <div className="text-red-500">Failed to load product.</div>
  if (!product) return <div>Product not found.</div>

  return (
    <div>
      <div className="flex flex-col md:flex-row gap-8 mb-8">
        <img src={product.images?.[0]} alt={product.name} className="rounded-xl w-full md:w-96 h-64 object-cover" />
        <div>
          <h2 className="text-3xl font-extrabold text-primary-600 mb-2">{product.name}</h2>
          <p className="text-gray-500 mb-2">{product.category} {product.brand && <>• {product.brand}</>}</p>
          <p className="mb-4">{product.description}</p>
          <div className="mb-4">
            <span className="font-bold text-lg text-primary-600">₹{product.variants?.[0]?.selling_price}</span>
            {product.variants?.[0]?.mrp > product.variants?.[0]?.selling_price && (
              <span className="line-through text-gray-400 ml-2">₹{product.variants?.[0]?.mrp}</span>
            )}
          </div>
          {/* Offers */}
          {loadingOffers ? <div className="animate-pulse">Loading offers...</div> : offers.length > 0 && (
            <div className="mb-4">
              <h4 className="font-bold text-primary-500 mb-2">Available Offers</h4>
              <ul className="list-disc ml-6">
                {offers.map((offer: any) => (
                  <li key={offer.offer_id} className="text-green-700 font-semibold">
                    {offer.name}: {offer.description}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
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

export default ProductDetailPage 