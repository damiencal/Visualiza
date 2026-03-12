import { useBreakpoints, breakpointsTailwind } from '@vueuse/core'

export const useBreakpoint = () => {
  const breakpoints = useBreakpoints(breakpointsTailwind)

  return {
    isMobile: breakpoints.smaller('md'),
    isTablet: breakpoints.between('md', 'lg'),
    isDesktop: breakpoints.greaterOrEqual('lg'),
    isSmallDesktop: breakpoints.between('lg', 'xl'),
    xl: breakpoints.greaterOrEqual('xl'),
    current: breakpoints.current(),
  }
}
