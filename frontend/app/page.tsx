'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    // 检查是否已登录
    const token = localStorage.getItem('token')
    const userStr = localStorage.getItem('user')
    if (token && userStr) {
      try {
        setUser(JSON.parse(userStr))
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.push('/login')
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-blue-50 to-white">
      <div className="z-10 max-w-5xl w-full items-center justify-center">
        {/* 导航栏 */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900">AI礼品推荐系统</h1>
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <span className="text-gray-700">
                  欢迎，<span className="font-semibold">{user.username}</span>
                  {user.role === 'admin' && <span className="ml-2 text-xs bg-red-100 text-red-800 px-2 py-1 rounded">管理员</span>}
                  {user.role === 'vip' && <span className="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">VIP</span>}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  退出登录
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="text-blue-600 hover:text-blue-800">
                  登录
                </Link>
                <Link
                  href="/register"
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  注册
                </Link>
              </>
            )}
          </div>
        </div>

        <div className="text-center mb-12">
          <p className="text-xl text-gray-600">
            基于AI的智能礼品推荐平台，帮您找到最合适的礼物
          </p>
        </div>

        <div className="flex gap-4 justify-center mb-16">
          <Link
            href="/recommend"
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors"
          >
            开始推荐
          </Link>
          <Link
            href="/products"
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-8 rounded-lg text-lg transition-colors"
          >
            浏览商品
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">智能推荐</h3>
            <p className="text-gray-600">
              基于AI算法，根据您的需求智能推荐最合适的礼品
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">多平台比价</h3>
            <p className="text-gray-600">
              聚合淘宝、京东、小红书等多个平台，一键比价
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">质量评级</h3>
            <p className="text-gray-600">
              多维度分析，为您提供专业的商品质量评级
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}