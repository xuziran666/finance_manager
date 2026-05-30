/**
 * 金额格式化工具函数
 * 将数字转换为人民币格式（如：¥100.00）
 */
export function fmt(v) {
  const n = parseFloat(v) || 0
  return '¥' + n.toFixed(2)
}
