/**
 * API 配置工具
 * 统一处理客户端和服务端的 API URL
 */

/**
 * 获取 API 基础 URL
 * - 客户端（浏览器）: 使用 localhost 或配置的 NEXT_PUBLIC_API_URL
 * - 服务端（SSR）: 使用容器内地址或配置的 BACKEND_URL
 */
export function getApiUrl(): string {
  // 如果是客户端环境（浏览器）
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
  
  // 如果是服务端环境（SSR）
  // 在 Docker 容器中，可以使用容器名访问
  return process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000'
}

/**
 * 构建完整的 API 端点 URL
 */
export function apiUrl(endpoint: string): string {
  const baseUrl = getApiUrl()
  // 确保 endpoint 以 / 开头
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  // 移除 baseUrl 末尾的斜杠，避免双斜杠
  const cleanBaseUrl = baseUrl.replace(/\/$/, '')
  return `${cleanBaseUrl}${path}`
}

