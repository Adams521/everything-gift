'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiUrl } from '@/lib/api'

interface RecommendationRequest {
  recipient_type?: string
  age_range?: string
  gender?: string
  relationship?: string
  occasion?: string
  budget_min?: number
  budget_max?: number
  style?: string
  mbti?: string
  zodiac?: string
  interests?: string[]
}

export default function RecommendPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<RecommendationRequest>({
    recipient_type: '',
    age_range: '',
    gender: '',
    relationship: '',
    occasion: '',
    budget_min: undefined,
    budget_max: undefined,
    style: '',
    mbti: '',
    zodiac: '',
    interests: [],
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch(apiUrl('/api/v1/recommendations'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('API Error:', response.status, errorText)
        throw new Error(`推荐失败: ${response.status}`)
      }

      const data = await response.json()
      console.log('Recommendation data:', data)
      
      // 跳转到结果页面
      router.push(`/results?data=${encodeURIComponent(JSON.stringify(data))}`)
    } catch (error) {
      console.error('Error:', error)
      alert(`推荐失败: ${error instanceof Error ? error.message : '请稍后重试'}`)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field: keyof RecommendationRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">AI礼品推荐</h1>
        
        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg px-8 pt-6 pb-8 mb-4">
          {/* 收礼人信息 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">收礼人信息</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  收礼人类型
                </label>
                <select
                  value={formData.recipient_type}
                  onChange={(e) => handleChange('recipient_type', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="男/女友">男/女友</option>
                  <option value="父母">父母</option>
                  <option value="同事">同事</option>
                  <option value="朋友">朋友</option>
                  <option value="客户">客户</option>
                  <option value="孩子">孩子</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  年龄段
                </label>
                <select
                  value={formData.age_range}
                  onChange={(e) => handleChange('age_range', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="18-25">18-25岁</option>
                  <option value="26-35">26-35岁</option>
                  <option value="36-45">36-45岁</option>
                  <option value="46-60">46-60岁</option>
                  <option value="60+">60岁以上</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  性别
                </label>
                <select
                  value={formData.gender}
                  onChange={(e) => handleChange('gender', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  关系
                </label>
                <select
                  value={formData.relationship}
                  onChange={(e) => handleChange('relationship', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="亲密">亲密</option>
                  <option value="熟悉">熟悉</option>
                  <option value="一般">一般</option>
                  <option value="商务">商务</option>
                </select>
              </div>
            </div>
          </div>

          {/* 场景和预算 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">场景和预算</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  场景用途
                </label>
                <select
                  value={formData.occasion}
                  onChange={(e) => handleChange('occasion', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="生日">生日</option>
                  <option value="纪念日">纪念日</option>
                  <option value="节日">节日</option>
                  <option value="毕业">毕业</option>
                  <option value="见家长">见家长</option>
                  <option value="商务往来">商务往来</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  风格偏好
                </label>
                <select
                  value={formData.style}
                  onChange={(e) => handleChange('style', e.target.value)}
                  className="w-full border rounded py-2 px-3"
                >
                  <option value="">请选择</option>
                  <option value="实用型">实用型</option>
                  <option value="创意型">创意型</option>
                  <option value="浪漫型">浪漫型</option>
                  <option value="搞笑型">搞笑型</option>
                  <option value="有仪式感">有仪式感</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  最低预算（元）
                </label>
                <input
                  type="number"
                  value={formData.budget_min || ''}
                  onChange={(e) => handleChange('budget_min', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full border rounded py-2 px-3"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  最高预算（元）
                </label>
                <input
                  type="number"
                  value={formData.budget_max || ''}
                  onChange={(e) => handleChange('budget_max', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full border rounded py-2 px-3"
                  placeholder="10000"
                />
              </div>
            </div>
          </div>

          {/* 提交按钮 */}
          <div className="flex items-center justify-center">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-8 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            >
              {loading ? '推荐中...' : '开始推荐'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
