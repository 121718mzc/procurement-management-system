import { describe, it, expect } from 'vitest'

// 模拟日期和ID转换函数
const formatDate = (date) => {
  if (!date) return date
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const parseDate = (dateString) => {
  if (!dateString) return null
  return new Date(dateString)
}

const convertToNumber = (value) => {
  if (value === null || value === undefined || value === '') return null
  return Number(value)
}

const convertToString = (value) => {
  if (value === null || value === undefined) return ''
  return String(value)
}

describe('通用功能测试', () => {
  describe('日期格式转换测试', () => {
    it('应该正确格式化日期对象', () => {
      const testDate = new Date('2026-03-05')
      const formattedDate = formatDate(testDate)
      expect(formattedDate).toBe('2026-03-05')
    })

    it('应该正确格式化日期字符串', () => {
      const testDateString = '2026-03-05'
      const formattedDate = formatDate(testDateString)
      expect(formattedDate).toBe('2026-03-05')
    })

    it('应该处理空日期', () => {
      expect(formatDate(null)).toBe(null)
      expect(formatDate(undefined)).toBe(undefined)
      expect(formatDate('')).toBe('')
    })

    it('应该正确解析日期字符串', () => {
      const testDateString = '2026-03-05'
      const parsedDate = parseDate(testDateString)
      expect(parsedDate).toBeInstanceOf(Date)
      expect(parsedDate.getFullYear()).toBe(2026)
      expect(parsedDate.getMonth()).toBe(2) // 月份从0开始
      expect(parsedDate.getDate()).toBe(5)
    })

    it('应该处理空日期字符串', () => {
      expect(parseDate(null)).toBe(null)
      expect(parseDate(undefined)).toBe(null)
      expect(parseDate('')).toBe(null)
    })
  })

  describe('ID类型转换测试', () => {
    it('应该正确将字符串转换为数字', () => {
      expect(convertToNumber('1')).toBe(1)
      expect(convertToNumber('123')).toBe(123)
      expect(convertToNumber('0')).toBe(0)
    })

    it('应该处理空值转换', () => {
      expect(convertToNumber(null)).toBe(null)
      expect(convertToNumber(undefined)).toBe(null)
      expect(convertToNumber('')).toBe(null)
    })

    it('应该正确将数字转换为字符串', () => {
      expect(convertToString(1)).toBe('1')
      expect(convertToString(123)).toBe('123')
      expect(convertToString(0)).toBe('0')
    })

    it('应该处理空值字符串转换', () => {
      expect(convertToString(null)).toBe('')
      expect(convertToString(undefined)).toBe('')
    })
  })

  describe('表单数据处理测试', () => {
    it('应该正确处理表单提交数据', () => {
      const formData = {
        id: '1',
        name: '测试',
        date: new Date('2026-03-05'),
        number: '100'
      }

      const processedData = {
        id: convertToNumber(formData.id),
        name: formData.name,
        date: formatDate(formData.date),
        number: convertToNumber(formData.number)
      }

      expect(processedData.id).toBe(1)
      expect(processedData.name).toBe('测试')
      expect(processedData.date).toBe('2026-03-05')
      expect(processedData.number).toBe(100)
    })

    it('应该处理表单空值', () => {
      const formData = {
        id: '',
        name: '',
        date: '',
        number: ''
      }

      const processedData = {
        id: convertToNumber(formData.id),
        name: formData.name,
        date: formatDate(formData.date),
        number: convertToNumber(formData.number)
      }

      expect(processedData.id).toBe(null)
      expect(processedData.name).toBe('')
      expect(processedData.date).toBe('')
      expect(processedData.number).toBe(null)
    })
  })

  describe('响应数据处理测试', () => {
    it('应该正确处理后端响应数据', () => {
      const mockResponse = {
        data: {
          id: 1,
          name: '测试',
          created_at: '2026-03-05 10:00:00',
          status: 'active'
        }
      }

      const processedData = {
        ...mockResponse.data,
        id: convertToString(mockResponse.data.id)
      }

      expect(processedData.id).toBe('1')
      expect(processedData.name).toBe('测试')
      expect(processedData.created_at).toBe('2026-03-05 10:00:00')
      expect(processedData.status).toBe('active')
    })

    it('应该处理嵌套响应数据', () => {
      const mockResponse = {
        data: {
          id: 1,
          name: '测试',
          items: [
            { id: 1, name: '项目1' },
            { id: 2, name: '项目2' }
          ]
        }
      }

      const processedData = {
        ...mockResponse.data,
        id: convertToString(mockResponse.data.id),
        items: mockResponse.data.items.map(item => ({
          ...item,
          id: convertToString(item.id)
        }))
      }

      expect(processedData.id).toBe('1')
      expect(processedData.items[0].id).toBe('1')
      expect(processedData.items[1].id).toBe('2')
    })
  })
})
