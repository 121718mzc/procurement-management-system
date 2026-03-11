// 通用工具函数

/**
 * 格式化日期为 YYYY-MM-DD 格式
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string|null} 格式化后的日期字符串
 */
export const formatDate = (date) => {
  if (!date) return null
  const d = new Date(date)
  if (isNaN(d.getTime())) return null
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/**
 * 解析日期字符串为日期对象
 * @param {string} dateString - 日期字符串
 * @returns {Date|null} 日期对象
 */
export const parseDate = (dateString) => {
  if (!dateString) return null
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return null
  return date
}

/**
 * 转换为数字类型
 * @param {any} value - 要转换的值
 * @returns {number|null} 转换后的数字
 */
export const toNumber = (value) => {
  if (value === null || value === undefined || value === '') return null
  const num = Number(value)
  return isNaN(num) ? null : num
}

/**
 * 转换为字符串类型
 * @param {any} value - 要转换的值
 * @returns {string} 转换后的字符串
 */
export const toString = (value) => {
  if (value === null || value === undefined) return ''
  return String(value)
}

/**
 * 转换表单数据类型
 * @param {Object} formData - 表单数据
 * @param {Object} fieldTypes - 字段类型配置
 * @returns {Object} 转换后的表单数据
 */
export const transformFormData = (formData, fieldTypes = {}) => {
  const transformed = { ...formData }
  
  Object.entries(fieldTypes).forEach(([field, type]) => {
    if (transformed.hasOwnProperty(field)) {
      switch (type) {
        case 'number':
          transformed[field] = toNumber(transformed[field])
          break
        case 'string':
          transformed[field] = toString(transformed[field])
          break
        case 'date':
          transformed[field] = formatDate(transformed[field])
          break
        case 'dateObject':
          transformed[field] = parseDate(transformed[field])
          break
      }
    }
  })
  
  return transformed
}

/**
 * 转换响应数据类型
 * @param {Object} data - 响应数据
 * @param {Object} fieldTypes - 字段类型配置
 * @returns {Object} 转换后的响应数据
 */
export const transformResponseData = (data, fieldTypes = {}) => {
  if (!data) return data
  
  const transformed = { ...data }
  
  Object.entries(fieldTypes).forEach(([field, type]) => {
    if (transformed.hasOwnProperty(field)) {
      switch (type) {
        case 'string':
          transformed[field] = toString(transformed[field])
          break
        case 'dateObject':
          transformed[field] = parseDate(transformed[field])
          break
      }
    }
  })
  
  return transformed
}

/**
 * 转换数组中每个对象的数据类型
 * @param {Array} array - 数据数组
 * @param {Object} fieldTypes - 字段类型配置
 * @returns {Array} 转换后的数组
 */
export const transformArrayData = (array, fieldTypes = {}) => {
  if (!Array.isArray(array)) return array
  return array.map(item => transformResponseData(item, fieldTypes))
}

/**
 * 生成唯一ID
 * @returns {string} 唯一ID
 */
export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 深拷贝对象
 * @param {any} obj - 要拷贝的对象
 * @returns {any} 拷贝后的对象
 */
export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime())
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (typeof obj === 'object') {
    const clonedObj = {}
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
}

/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要执行的函数
 * @param {number} limit - 时间限制（毫秒）
 * @returns {Function} 节流后的函数
 */
export const throttle = (func, limit) => {
  let inThrottle
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}
