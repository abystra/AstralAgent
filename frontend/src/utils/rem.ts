/**
 * 移动端 rem 适配
 * 
 * 根据设备宽度动态设置根元素字体大小
 * 设计稿基准：375px
 */

(function setRem() {
  const baseSize = 16 // 基准字体大小（px）
  const baseWidth = 375 // 设计稿基准宽度（px）

  function setRemUnit() {
    const scale = document.documentElement.clientWidth / baseWidth
    const fontSize = baseSize * Math.min(scale, 2) // 最大不超过 2 倍
    document.documentElement.style.fontSize = `${fontSize}px`
  }

  setRemUnit()

  // 监听窗口大小变化
  window.addEventListener('resize', setRemUnit)
  // 监听屏幕旋转
  window.addEventListener('orientationchange', setRemUnit)
})()

