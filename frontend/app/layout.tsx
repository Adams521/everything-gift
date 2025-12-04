import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI礼品推荐系统',
  description: '基于AI的智能礼品推荐平台',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  )
}
