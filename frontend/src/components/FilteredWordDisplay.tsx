// The sentences in view: every sentence of the capture, or the members of the selected node or
// link, a page at a time, each with its target word highlighted in its label's colour. Clicking a
// sentence selects it, so its path lights up in the charts (DESIGN.md E5); a search box finds one
// by its text or id among those loaded.
import { useEffect, useRef, useState } from 'react'
import type { ProbeExample } from '../types/api'
import { valueColor, type GradientScheme } from '../color/scheme'
import SentenceHighlight from './SentenceHighlight'

interface FilteredWordDisplayProps {
  sentences: ProbeExample[]
  heading: string
  targetWord?: string
  total?: number // when more exist than are loaded
  onLoadMore?: () => void
  isLoading?: boolean
  labelValues: string[] // the label axis's values, so each label keeps its colour
  gradient: GradientScheme
  onPick?: (probeId: string) => void // select one sentence
  pickedId?: string // the selected sentence, ringed
}

export default function FilteredWordDisplay({
  sentences,
  heading,
  targetWord,
  total,
  onLoadMore,
  isLoading = false,
  labelValues,
  gradient,
  onPick,
  pickedId,
}: FilteredWordDisplayProps) {
  const [query, setQuery] = useState('')
  // A sentence picked elsewhere (a 3-D point, the URL) is scrolled into view
  const pickedRow = useRef<HTMLDivElement>(null)
  useEffect(() => { pickedRow.current?.scrollIntoView({ block: 'nearest' }) }, [pickedId])
  const needle = query.trim().toLowerCase()
  const shown = needle
    ? sentences.filter(s => s.input_text?.toLowerCase().includes(needle) || s.probe_id.toLowerCase().includes(needle))
    : sentences
  const count = total ?? sentences.length

  return (
    <div className="bg-white rounded-xl shadow-md p-2 space-y-1">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900 text-xs">
          {heading} {targetWord && <span className="text-gray-500 font-normal">— {targetWord}</span>}
        </h4>
        <span className="flex items-center gap-2 text-[10px] text-gray-500">
          {onPick && (
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="find a sentence…"
              aria-label="Find a sentence by its text or id"
              className="px-1 py-0.5 w-40 text-[10px] border border-gray-300 rounded bg-white" />
          )}
          {needle ? `${shown.length} found in ${sentences.length}` : sentences.length < count ? `${sentences.length} of ${count}` : count}
        </span>
      </div>

      {/* Sentence List */}
      {shown.length > 0 ? (
        <div className="space-y-0.5 max-h-[75vh] overflow-y-auto">
          {shown.map((sentence, i) => {
            const color = sentence.label && labelValues.length > 0
              ? valueColor(sentence.label, labelValues, gradient)
              : '#666666'

            // Use last occurrence for highlighting — target_char_offset from old captures can be wrong
            const lastIdx = sentence.input_text?.toLowerCase().lastIndexOf((sentence.target_word || '').toLowerCase()) ?? -1
            const offset = lastIdx >= 0 ? lastIdx : sentence.target_char_offset
            const fullText = sentence.input_text
            let displayText = fullText
            let displayOffset = offset
            const WINDOW = 80

            if (offset != null && fullText.length > WINDOW * 2 + sentence.target_word.length) {
              const start = Math.max(0, offset - WINDOW)
              const end = Math.min(fullText.length, offset + sentence.target_word.length + WINDOW)
              displayText = (start > 0 ? '...' : '') + fullText.slice(start, end) + (end < fullText.length ? '...' : '')
              displayOffset = offset - start + (start > 0 ? 3 : 0)
            }

            return (
              <div key={sentence.probe_id || i} ref={pickedId === sentence.probe_id ? pickedRow : undefined} onClick={onPick ? () => onPick(sentence.probe_id) : undefined}
                title={onPick ? 'Select this sentence: its path lights up in the charts' : undefined}
                className={`rounded px-1.5 py-1 ${pickedId === sentence.probe_id ? 'bg-amber-50 ring-1 ring-amber-400' : 'bg-gray-50'}
                  ${onPick ? 'cursor-pointer hover:bg-blue-50' : ''}`}>
                <p className="text-[10px] text-gray-700 leading-snug">
                  {sentence.label && (
                    <span
                      className="inline-block px-1 py-px text-[8px] font-medium rounded text-white capitalize mr-1 align-middle"
                      style={{ backgroundColor: color }}
                    >
                      {sentence.label}
                    </span>
                  )}
                  {sentence.capture_type === 'generation' && (
                    <span className="inline-block px-1 py-px text-[8px] font-medium rounded bg-purple-500 text-white mr-1 align-middle">
                      gen
                    </span>
                  )}
                  <SentenceHighlight
                    text={displayText}
                    targetWord={sentence.target_word}
                    color={color}
                    charOffset={displayOffset}
                  />
                </p>
              </div>
            )
          })}
        </div>
      ) : (
        <p className="text-[10px] text-gray-500">
          {isLoading ? 'Loading…' : needle ? 'No sentence matches' : 'No sentences'}
        </p>
      )}
      {onLoadMore && sentences.length < count && (
        <button onClick={onLoadMore} disabled={isLoading}
          className="w-full text-[10px] text-blue-700 hover:underline disabled:text-gray-400 py-1">
          {isLoading ? 'Loading…' : `Show ${Math.min(50, count - sentences.length)} more`}
        </button>
      )}
    </div>
  )
}
