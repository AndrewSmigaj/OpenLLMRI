// Tokens with their scores (the score on hover). Tokens often start with a space or hold a line
// break; both are shown.
import type { TokenScore } from '../../types/lens'

const shown = (token: string) => token.replace(/ /g, '␣').replace(/\n/g, '⏎')

export default function Tokens({ tokens, unit }: { tokens: TokenScore[]; unit: string }) {
  return (
    <div className="flex flex-wrap gap-1">
      {tokens.map(([token, value], i) => (
        <span key={i} title={`${unit} ${value}`}
          className="font-mono text-[10px] bg-gray-100 border border-gray-200 rounded px-1">{shown(token)}</span>
      ))}
    </div>
  )
}
