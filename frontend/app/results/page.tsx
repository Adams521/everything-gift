'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Product {
  id: number
  name: string
  price: number | null
  image_url: string | null
  platform: string
  platform_url: string
  description: string | null
}

interface RecommendationResponse {
  categories: string[]
  products: Product[]
  reasoning: string
}

export default function ResultsPage() {
  const searchParams = useSearchParams()
  const [data, setData] = useState<RecommendationResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const dataParam = searchParams.get('data')
    if (dataParam) {
      try {
        const parsed = JSON.parse(decodeURIComponent(dataParam))
        setData(parsed)
      } catch (error) {
        console.error('Error parsing data:', error)
      }
    }
    setLoading(false)
  }, [searchParams])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">加载中...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">未找到推荐结果</h1>
          <Link href="/recommend" className="text-blue-500 hover:underline">
            返回推荐页面
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <Link href="/recommend" className="text-blue-500 hover:underline mb-4 inline-block">
            ← 返回推荐
          </Link>
          <h1 className="text-3xl font-bold mb-4">推荐结果</h1>
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
            <p className="text-gray-700">{data.reasoning}</p>
          </div>
        </div>

        {data.categories.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">推荐品类</h2>
            <div className="flex flex-wrap gap-2">
              {data.categories.map((category, index) => (
                <span
                  key={index}
                  className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm"
                >
                  {category}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">推荐商品</h2>
          {data.products.length === 0 ? (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
              <p className="text-yellow-800">暂无推荐商品，请尝试调整筛选条件。</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.products.map((product) => (
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
    </div>
  )
}
