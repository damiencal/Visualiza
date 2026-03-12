export function formatPrice(amount: number, currency: 'DOP' | 'USD' = 'DOP'): string {
  if (currency === 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  // Dominican Peso formatting
  return new Intl.NumberFormat('es-DO', {
    style: 'currency',
    currency: 'DOP',
    maximumFractionDigits: 0,
  }).format(amount)
}

export function formatCompactPrice(amount: number, currency: 'DOP' | 'USD' = 'DOP'): string {
  const symbol = currency === 'USD' ? '$' : 'RD$'
  if (amount >= 1_000_000) {
    return `${symbol}${(amount / 1_000_000).toFixed(1)}M`
  }
  if (amount >= 1_000) {
    return `${symbol}${(amount / 1_000).toFixed(0)}K`
  }
  return `${symbol}${amount}`
}
