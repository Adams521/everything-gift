'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { apiUrl } from '@/lib/api'

interface Product {
  id: number
  name: string
  price: number | null
  image_url: string | null
  platform: string
  platform_url: string
  description: string | null
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await fetch(
        apiUrl('/api/v1/products?limit=20')
      )
      
      if (!response.ok) {
        throw new Error('获取商品失败')
      }
      
      const data = await response.json()
      setProducts(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">加载中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4 text-red-600">错误</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchProducts}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
          >
            重试
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <Link href="/" className="text-blue-500 hover:underline mb-4 inline-block">
            ← 返回首页
          </Link>
          <h1 className="text-3xl font-bold mb-4">商品列表</h1>
        </div>

        {products.length === 0 ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
            <p className="text-yellow-800">暂无商品数据。</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <div
                key={product.id}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
              >
                <div className="w-full h-48 bg-gray-200 flex items-center justify-center overflow-hidden">
                  {product.image_url ? (
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        // 图片加载失败时使用默认图片
                        e.currentTarget.src = 'https://via.placeholder.com/300x300?text=No+Image'
                        e.currentTarget.onerror = null
                      }}
                    />
                  ) : (
                    <div className="text-gray-400 text-sm">暂无图片</div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
                  {product.description && (
                    <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                      {product.description}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    {product.price && (
                      <span className="text-xl font-bold text-blue-600">
                        ¥{product.price.toFixed(2)}
                      </span>
                    )}
                    <span className="text-sm text-gray-500">{product.platform}</span>
                  </div>
                  <a
                    href={product.platform_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-4 block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
                  >
                    查看详情
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
