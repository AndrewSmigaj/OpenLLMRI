// The ECharts option for a Sankey chart, built from flows as a pure function so the colouring, the
// lighting and the link trim can be tested without a browser. SankeyChart draws it.
import * as echarts from 'echarts';
import type { SankeyNode, SankeyLink } from '../../types/api';
import { answerColours, distColor, stripeStops, type AxisCounts, type ColourSpec } from '../../color/scheme';
import { isOutputNode, isOutputLink, stripOutputPrefix, OUTPUT_NODE_PREFIX } from '../../constants/outputNodes';
import { linkKey, litOpacity, type Lit } from '../../utils/lighting';

// The node and link objects this chart gives ECharts, as they come back in event and tooltip params
export type SankeyItemRef = { name?: string; id?: string; source?: string; target?: string };

// How nodes and links are coloured: by the input spec; the output column by its own spec, or
// without one by matching its categories to the input's colours. Stripes show exact shares.
export interface SankeyColours {
  input: ColourSpec;
  output: ColourSpec | null;
  stripes: boolean;
}

export interface SankeyOptionInput {
  nodes: SankeyNode[];
  links: SankeyLink[];
  colours: SankeyColours;
  nodeWidth: number;
  // The series' margins, in pixels or as a percentage string
  left: number | string;
  right: number | string;
  showLabels: boolean;
  // Nodes to outline, with a count each (nodes holding items raw space groups differently)
  outlined?: Record<string, number>;
  // What a selection lights (utils/lighting): lit nodes and links keep their colours, links by their
  // share of the lit items; the rest fade. Node sizes don't change, so nothing moves.
  lit?: Lit | null;
  // Nodes and links only read items take (utils/lighting ghostFlows), drawn grey and dashed
  ghosts?: Lit | null;
}

const GHOST = '#9ca3af';

// A faded node's and a faded link's opacity while something is lit
export const FADED_NODE = 0.2;
export const FADED_LINK = 0.04;

const countsOf = (item: SankeyNode | SankeyLink): AxisCounts =>
  ({ label: item.label_distribution ?? {}, ...(item.category_distributions ?? {}) });

// Busier links are wider and more opaque (square-root scale)
function trafficStyle(value: number, maxValue: number): { opacity: number; lineWidth: number } {
  if (maxValue <= 0) return { opacity: 0.3, lineWidth: 1 };
  const share = Math.sqrt(value) / Math.sqrt(maxValue);
  return { opacity: 0.3 + share * 0.6, lineWidth: 1 + share * 5 };
}

// The strongest `n` links leaving each layer, plus every link into the output column and every
// lit link (a selection's path is drawn whole).
export function topLinks(links: SankeyLink[], n: number, lit?: Lit | null): SankeyLink[] {
  const byLayer = new Map<string, SankeyLink[]>();
  const kept: SankeyLink[] = [];
  for (const link of links) {
    if (isOutputLink(link) || lit?.links[linkKey(link.source, link.target)]) { kept.push(link); continue; }
    const layer = /^L(\d+)/.exec(link.source)?.[1] ?? '';
    byLayer.set(layer, [...(byLayer.get(layer) ?? []), link]);
  }
  for (const group of byLayer.values()) {
    kept.push(...[...group].sort((a, b) => b.value - a.value).slice(0, n));
  }
  return kept;
}

export function sankeyOption({ nodes, links, colours, nodeWidth, left, right, showLabels, outlined, lit, ghosts }: SankeyOptionInput): echarts.EChartsOption {
  const { input, output, stripes } = colours;

  // Compute depth offset for proper column placement
  const minLayer = nodes.length > 0 ? Math.min(...nodes.map(n => n.layer)) : 0;

  // Without an output spec, output categories take the input's colours by name (answerColours)
  const answers = answerColours(input, nodes.filter(n => isOutputNode(n.name)).map(n => stripOutputPrefix(n.name)));

  const nodeColor = (node: SankeyNode): string | echarts.graphic.LinearGradient => {
    if (isOutputNode(node.name)) {
      return output
        ? distColor(node.output_distributions ?? {}, output)
        : answers[stripOutputPrefix(node.name)];
    }
    if (!stripes) return distColor(countsOf(node), input);
    // Bands top to bottom, in the axis's order; a gradient with hard stops
    return new echarts.graphic.LinearGradient(0, 0, 0, 1, stripeStops(countsOf(node), input));
  };
  const linkColor = (link: SankeyLink): string =>
    isOutputLink(link) && output
      ? distColor(link.output_distributions ?? {}, output)
      : distColor(countsOf(link), input);

  const lighting = lit && lit.total > 0 ? lit : null;
  const sankeyNodes = nodes.map(node => ({
    id: node.id,
    name: node.name,
    value: Math.max(1, node.token_count),
    depth: node.layer - minLayer,
    itemStyle: {
      color: nodeColor(node),
      ...(outlined?.[node.id] ? { borderColor: '#111827', borderWidth: 2 } : {}),
      ...(lighting ? { opacity: lighting.nodes[node.id] ? 1 : FADED_NODE } : {}),
    },
  }));

  // Ghosts: a node's column from its id (the output column after the last layer)
  const maxLayer = nodes.length > 0 ? Math.max(...nodes.map(n => n.layer)) : 0;
  const outputDepth = nodes.some(n => isOutputNode(n.name)) ? Math.max(...nodes.filter(n => isOutputNode(n.name)).map(n => n.layer)) - minLayer
    : maxLayer - minLayer + 1;
  const ghostNodes = Object.entries(ghosts?.nodes ?? {}).map(([id, count]) => ({
    id, name: id, value: count, ghost: count,
    depth: isOutputNode(id) ? outputDepth : Number(/^L(\d+)/.exec(id)?.[1] ?? minLayer) - minLayer,
    itemStyle: {
      color: '#f3f4f6', borderColor: GHOST, borderType: 'dashed' as const, borderWidth: 1,
      ...(lighting ? { opacity: lighting.nodes[id] ? 1 : FADED_NODE } : {}),
    },
  }));

  const maxLinkValue = Math.max(...links.map(l => l.value));
  const sankeyLinks = links.map(link => {
    const { opacity, lineWidth } = trafficStyle(link.value, maxLinkValue);
    const count = lighting?.links[linkKey(link.source, link.target)];
    return {
      source: link.source,
      target: link.target,
      value: Math.max(0.5, link.value),
      lineStyle: {
        color: linkColor(link), width: lineWidth, curveness: 0.3,
        opacity: lighting ? (count ? litOpacity(count, lighting.total) : FADED_LINK) : opacity,
      },
    };
  });
  const ghostLinks = Object.entries(ghosts?.links ?? {}).map(([key, value]) => {
    const [source, target] = key.split('>');
    const count = lighting?.links[key];
    return {
      source, target, value, ghost: value,
      lineStyle: {
        color: GHOST, type: 'dashed' as const, width: 1, curveness: 0.3,
        opacity: lighting ? (count ? litOpacity(count, lighting.total) : FADED_LINK) : 0.35,
      },
    };
  });

  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (Array.isArray(params)) return '';
        const item = params.data as SankeyItemRef;
        const ghost = (params.data as { ghost?: number }).ghost;
        if (ghost !== undefined) {
          const isNode = params.dataType === 'node';
          const id = isNode ? String(item.name) : linkKey(String(item.source), String(item.target));
          const litCount = lighting?.[isNode ? 'nodes' : 'links'][id];
          return `
            <div style="max-width: 300px;">
              <strong>${isNode ? item.name : `${item.source} → ${item.target}`}</strong><br/>
              <hr style="margin: 4px 0;"/>
              Only read items take this: ${ghost} of the ${ghosts?.total ?? 0} read; no lens item does<br/>
              ${litCount ? `Lit: ${litCount} of the ${lighting?.total} lit items<br/>` : ''}
            </div>
          `;
        }
        if (params.dataType === 'node') {
          const node = nodes.find(n => n.name === item.name);
          if (!node) return '';

          // Output node tooltip
          if (isOutputNode(node.name)) {
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
              ${lighting?.nodes[node.id] ? `Lit: ${lighting.nodes[node.id]} of the ${lighting.total} lit items<br/>` : ''}
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
              ${lighting?.links[linkKey(link.source, link.target)] ? `Lit: ${lighting.links[linkKey(link.source, link.target)]} of the ${lighting.total} lit items<br/>` : ''}
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
      data: [...sankeyNodes, ...ghostNodes],
      links: [...sankeyLinks, ...ghostLinks],
      nodeAlign: 'justify',
      nodeGap: 8,
      nodeWidth,
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
}
