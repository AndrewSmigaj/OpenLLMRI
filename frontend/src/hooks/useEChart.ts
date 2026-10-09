// One ECharts chart in a box: created once, given each new option whole, disposed with the box.
import { useEffect, useRef } from 'react'
import * as echarts from 'echarts'

export function useEChart(option: echarts.EChartsOption | null) {
  const box = useRef<HTMLDivElement>(null)
  const chart = useRef<echarts.ECharts | null>(null)
  useEffect(() => {
    if (!box.current || !option) return
    chart.current ??= echarts.init(box.current)
    chart.current.setOption(option, true)
  }, [option])
  useEffect(() => () => { chart.current?.dispose(); chart.current = null }, [])
  return box
}
