import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { SankeyNode, SankeyLink } from '../../types/api';
import { answerColours, distColor, stripeStops, type AxisCounts, type ColourSpec } from '../../color/scheme';
import { isOutputNode as checkIsOutputNode, isOutputLink as checkIsOutputLink, stripOutputPrefix, OUTPUT_NODE_PREFIX } from '../../constants/outputNodes';

// The node and link objects this chart gives ECharts, as they come back in event and tooltip params
type SankeyItemRef = { name?: string; id?: string; source?: string; target?: string };

// How nodes and links are coloured: by the input spec; the output column by its own spec, or
// without one by matching its categories to the input's colours. Stripes show exact shares.
export interface SankeyColours {
  input: ColourSpec;
  output: ColourSpec | null;
  stripes: boolean;
}

const countsOf = (item: SankeyNode | SankeyLink): AxisCounts =>
  ({ label: item.label_distribution ?? {}, ...(item.category_distributions ?? {}) });

// Busier links are wider and more opaque (square-root scale)
function trafficStyle(value: number, maxValue: number): { opacity: number; lineWidth: number } {
  if (maxValue <= 0) return { opacity: 0.3, lineWidth: 1 };
  const share = Math.sqrt(value) / Math.sqrt(maxValue);
  return { opacity: 0.3 + share * 0.6, lineWidth: 1 + share * 5 };
}

interface SankeyChartProps {
  nodes: SankeyNode[];
  colours: SankeyColours;
  links: SankeyLink[];
  onNodeClick?: (nodeId: string, nodeData: SankeyNode) => void;
  onLinkClick?: (linkData: SankeyLink) => void;
  height?: number;
  width?: number;
  nodeWidth?: number;
  // The series' margins, in pixels or as a percentage string; charts that must line up share them
  left?: number | string;
  right?: number | string;
  showLabels?: boolean;
  // Nodes to outline, with a count each (nodes holding items raw space groups differently)
  outlined?: Record<string, number>;
  // The ECharts instance once it exists (null when it goes), for exports
  onChartReady?: (chart: echarts.ECharts | null) => void;
}

const SankeyChart: React.FC<SankeyChartProps> = ({
  nodes,
  links,
  colours,
  onNodeClick,
  onLinkClick,
  height = 600,
  width = 800,
  nodeWidth: nodeWidthProp = 6,
  left = '2%',
  right = '30%',
  showLabels = true,
  outlined,
  onChartReady,
}) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const nodesRef = useRef(nodes);
  const linksRef = useRef(links);
  const onNodeClickRef = useRef(onNodeClick);
  const onLinkClickRef = useRef(onLinkClick);
  const onChartReadyRef = useRef(onChartReady);

  // Update refs when props change
  nodesRef.current = nodes;
  linksRef.current = links;
  onNodeClickRef.current = onNodeClick;
  onLinkClickRef.current = onLinkClick;
  onChartReadyRef.current = onChartReady;

  useEffect(() => {
    if (!chartRef.current) return;

    // Initialize chart. A wide all-layer chart is thousands of pixels across, so the pixel ratio
    // is capped to keep the canvas within browser limits.
    chartInstance.current = echarts.init(chartRef.current, undefined, {
      devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
    });
    onChartReadyRef.current?.(chartInstance.current);

    // Handle click events
    const handleClick = (params: echarts.ECElementEvent) => {
      const item = params.data as SankeyItemRef;
      if (params.dataType === 'node' && onNodeClickRef.current) {
        // Match by name — ECharts Sankey uses name as the node key
        const nodeName = item.name || item.id;
        const node = nodesRef.current.find(n => n.name === nodeName || n.id === nodeName);
        if (node) {
          onNodeClickRef.current(node.id, node);
        }
      } else if (params.dataType === 'edge' && onLinkClickRef.current) {
        const link = linksRef.current.find(l =>
          l.source === item.source && l.target === item.target
        );
        if (link) {
          onLinkClickRef.current(link);
        }
      }
    };

    chartInstance.current.on('click', handleClick);

    // Handle resize — observe container, not just window
    // Use requestAnimationFrame to avoid resize during ECharts main process
    const handleResize = () => {
      requestAnimationFrame(() => {
        chartInstance.current?.resize();
      });
    };
    window.addEventListener('resize', handleResize);

    const resizeObserver = new ResizeObserver(() => {
      requestAnimationFrame(() => {
        chartInstance.current?.resize();
      });
    });
    resizeObserver.observe(chartRef.current);

    return () => {
      chartInstance.current?.off('click', handleClick);
      window.removeEventListener('resize', handleResize);
      resizeObserver.disconnect();
      onChartReadyRef.current?.(null);
      chartInstance.current?.dispose();
    };
  }, []);

  // Resize chart when container dimensions might change
  useEffect(() => {
    const resizeChart = () => {
      if (chartInstance.current) {
        setTimeout(() => {
          chartInstance.current?.resize();
        }, 100);
      }
    };

    resizeChart();
  }, [width, height]);

  // Update chart when data or colors change
  useEffect(() => {
    if (!chartInstance.current) return;

    const { input, output, stripes } = colours;

    // Compute depth offset for proper column placement
    const minLayer = nodes.length > 0 ? Math.min(...nodes.map(n => n.layer)) : 0;

    // Without an output spec, output categories take the input's colours by name (answerColours)
    const answers = answerColours(input, nodes.filter(n => checkIsOutputNode(n.name)).map(n => stripOutputPrefix(n.name)));

    const nodeColor = (node: SankeyNode): string | echarts.graphic.LinearGradient => {
      if (checkIsOutputNode(node.name)) {
        return output
          ? distColor(node.output_distributions ?? {}, output)
          : answers[stripOutputPrefix(node.name)];
      }
      if (!stripes) return distColor(countsOf(node), input);
      // Bands top to bottom, in the axis's order; a gradient with hard stops
      return new echarts.graphic.LinearGradient(0, 0, 0, 1, stripeStops(countsOf(node), input));
    };
    const linkColor = (link: SankeyLink): string =>
      checkIsOutputLink(link) && output
        ? distColor(link.output_distributions ?? {}, output)
        : distColor(countsOf(link), input);

    const sankeyNodes = nodes.map(node => ({
      id: node.id,
      name: node.name,
      value: Math.max(1, node.token_count),
      depth: node.layer - minLayer,
      itemStyle: outlined?.[node.id]
        ? { color: nodeColor(node), borderColor: '#111827', borderWidth: 2 }
        : { color: nodeColor(node) },
    }));

    const maxLinkValue = Math.max(...links.map(l => l.value));
    const sankeyLinks = links.map(link => {
      const { opacity, lineWidth } = trafficStyle(link.value, maxLinkValue);
      return {
        source: link.source,
        target: link.target,
        value: Math.max(0.5, link.value),
        lineStyle: { color: linkColor(link), opacity, width: lineWidth, curveness: 0.3 },
      };
    });

    const option: echarts.EChartsOption = {
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          if (Array.isArray(params)) return '';
          const item = params.data as SankeyItemRef;
          if (params.dataType === 'node') {
            const node = nodes.find(n => n.name === item.name);
            if (!node) return '';

            // Output node tooltip
            if (checkIsOutputNode(node.name)) {
              const category = stripOutputPrefix(node.name);
              return `
                <div style="max-width: 300px;">
                  <strong>${OUTPUT_NODE_PREFIX}${category}</strong><br/>
                  <hr style="margin: 4px 0;"/>
                  Probes: ${node.token_count}<br/>
                  Labels: ${node.label_distribution ? Object.entries(node.label_distribution).map(([k, v]) => `${k}: ${v}`).join(', ') : 'N/A'}
                  ${node.category_distributions ? '<br/>Categories: ' + Object.entries(node.category_distributions).map(([axis, dist]) => `${axis}: ${Object.entries(dist).map(([k, v]) => `${k}(${v})`).join(', ')}`).join('; ') : ''}
                </div>
              `;
            }

            return `
              <div style="max-width: 300px;">
                <strong>${node.name}</strong><br/>
                <hr style="margin: 4px 0;"/>
                ${/^L\d+C\d+$/.test(node.id) ? 'Cluster' : 'Expert'}: ${node.expert_id}<br/>
                Layer: ${node.layer}<br/>
                Token Count: ${node.token_count}<br/>
                ${outlined?.[node.id] ? `Outlined: ${outlined[node.id]} of its items are grouped differently in raw space<br/>` : ''}
                Labels: ${node.label_distribution ? Object.entries(node.label_distribution).map(([k, v]) => `${k}: ${v}`).join(', ') : 'N/A'}
              </div>
            `;
          } else if (params.dataType === 'edge') {
            const link = links.find(l => l.source === item.source && l.target === item.target);
            if (!link) return '';
            return `
              <div style="max-width: 300px;">
                <strong>Route</strong><br/>
                <hr style="margin: 4px 0;"/>
                ${link.source} → ${link.target}<br/>
                Flow: ${link.value} tokens<br/>
                Route: ${link.route_signature}
              </div>
            `;
          }
          return '';
        }
      },
      series: [{
        type: 'sankey',
        emphasis: {
          focus: 'adjacency',
          label: {
            fontWeight: 'bold',
            fontSize: 11,
            color: '#1f2937'
          }
        },
        data: sankeyNodes,
        links: sankeyLinks,
        nodeAlign: 'justify',
        nodeGap: 8,
        nodeWidth: nodeWidthProp,
        layoutIterations: 0,
        left,
        right,
        top: '2%',
        bottom: '2%',
        label: {
          show: showLabels,
          position: 'right',
          fontSize: 11,
          color: '#1f2937',
          // The output column shows its categories without the "Generated:" prefix
          formatter: (params) => stripOutputPrefix(params.name || '')
        }
      }],
      animation: true,
      animationDuration: 1000
    };

    chartInstance.current.setOption(option);
  }, [nodes, links, colours, left, right, showLabels, nodeWidthProp, outlined]);

  return (
    <div
      ref={chartRef}
      style={{ width: '100%', height: `${height}px` }}
      className="sankey-chart border border-gray-200 rounded-lg bg-white"
    />
  );
};

export default SankeyChart;
