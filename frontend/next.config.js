/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // 允许外部图片域名
  images: {
    domains: [
      'localhost',
      'images.unsplash.com',
      'via.placeholder.com',
      'img.alicdn.com',
      'img14.360buyimg.com',
    ],
    unoptimized: true,
  },
}

module.exports = nextConfig