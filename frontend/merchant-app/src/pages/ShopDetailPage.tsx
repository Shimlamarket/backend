import React from 'react'
import { useParams } from 'react-router-dom'

const ShopDetailPage: React.FC = () => {
  const { shopId } = useParams()
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Shop Details</h2>
      <p className="text-gray-600">Details for shop <span className="font-mono">{shopId}</span> will appear here. (Coming soon!)</p>
    </div>
  )
}

export default ShopDetailPage 