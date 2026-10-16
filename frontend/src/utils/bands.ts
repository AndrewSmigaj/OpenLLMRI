// A shaded band from a low line to a high line on an ECharts line chart, for a score's range over a
// search's test draws (DESIGN.md C4, LENS-21): a transparent floor at the low values with the band's
// width stacked on it. 'all' stacking keeps a band right where the low values are below zero.
import type * as echarts from 'echarts'

export function bandSeries(name: string, low: (number | null)[], high: (number | null)[], color: string,
  stack: string): echarts.LineSeriesOption[] {
  const width = low.map((lo, i) => (lo === null || high[i] === null || high[i] === undefined ? null : (high[i] as number) - lo))
  return [
    { name: `${name} (floor)`, type: 'line', data: low, stack, stackStrategy: 'all', symbol: 'none', silent: true,
      lineStyle: { opacity: 0 }, tooltip: { show: false } },
    { name, type: 'line', data: width, stack, stackStrategy: 'all', symbol: 'none', silent: true,
      lineStyle: { opacity: 0 }, areaStyle: { color, opacity: 0.15 }, itemStyle: { color }, tooltip: { show: false } },
  ]
}

// The legend entries of a chart's series, leaving out the bands' floors
export const legendNames = (series: { name?: string | number }[]) =>
  series.map(s => String(s.name ?? '')).filter(name => name && !name.endsWith(' (floor)'))
