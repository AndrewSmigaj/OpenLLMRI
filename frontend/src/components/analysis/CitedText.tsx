// A card's sentence with its citations as chips: hovering one shows the facts it names and their
// values, which the number checker compared with the numbers before it.
import type { ReactNode } from 'react'
import type { Fact } from '../../types/cards'

const CITE = /\[(F\d+(?:\s*,\s*F\d+)*)\]/g

export default function CitedText({ text, facts }: { text: string; facts: Record<string, Fact> }) {
  const parts: ReactNode[] = []
  let last = 0
  for (const match of text.matchAll(CITE)) {
    const at = match.index ?? 0
    const ids = match[1].split(/\s*,\s*/)
    parts.push(text.slice(last, at))
    parts.push(
      <span key={at} title={ids.map(id => (facts[id] ? `${id}: ${facts[id].what} = ${facts[id].value}` : `${id}: not a fact`)).join('\n')}
        className="mx-0.5 px-0.5 rounded bg-violet-100 text-violet-800 text-[9px] font-mono align-baseline cursor-help">
        {ids.join(',')}
      </span>)
    last = at + match[0].length
  }
  parts.push(text.slice(last))
  return <>{parts}</>
}
