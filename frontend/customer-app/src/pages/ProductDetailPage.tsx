import React from 'react'
import { useParams } from 'react-router-dom'

const ProductDetailPage: React.FC = () => {
  const { productId } = useParams()
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Product Details</h2>
      <p className="text-gray-600">Details for product <span className="font-mono">{productId}</span> will appear here. (Coming soon!)</p>
    </div>
  )
}

export default ProductDetailPage 