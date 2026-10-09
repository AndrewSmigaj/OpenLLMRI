import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { SankeyNode, SankeyLink } from '../../types/api';
import type { Lit } from '../../utils/lighting';
import { sankeyOption, type SankeyColours, type SankeyItemRef } from './sankeyOption';

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
  // What a selection lights (utils/lighting): lit nodes and links keep their colours, links by their
  // share of the lit items; the rest fade. Node sizes don't change, so nothing moves.
  lit?: Lit | null;
  // Nodes and links only read items take, drawn grey and dashed (utils/lighting ghostFlows)
  ghosts?: Lit | null;
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
  lit,
  ghosts,
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

    chartInstance.current.setOption(sankeyOption({
      nodes, links, colours, nodeWidth: nodeWidthProp, left, right, showLabels, outlined, lit, ghosts,
    }));
  }, [nodes, links, colours, left, right, showLabels, nodeWidthProp, outlined, lit, ghosts]);

  return (
    <div
      ref={chartRef}
      style={{ width: '100%', height: `${height}px` }}
      className="sankey-chart border border-gray-200 rounded-lg bg-white"
    />
  );
};

export default SankeyChart;
