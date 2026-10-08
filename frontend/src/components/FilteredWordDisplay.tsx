// The sentences in view: every sentence of the capture, or the members of the selected node or
// link, a page at a time, each with its target word highlighted in its label's colour.
import type { ProbeExample } from '../types/api'
import type { GradientScheme } from '../utils/colorBlending'
import { getNodeColor } from '../utils/colorBlending'
import SentenceHighlight from './SentenceHighlight'

interface FilteredWordDisplayProps {
  sentences: ProbeExample[]
  heading: string
  targetWord?: string
  total?: number // when more exist than are loaded
  onLoadMore?: () => void
  isLoading?: boolean
  primaryValues: string[]
  gradient: GradientScheme
}

export default function FilteredWordDisplay({
  sentences,
  heading,
  targetWord,
  total,
  onLoadMore,
  isLoading = false,
  primaryValues,
  gradient
}: FilteredWordDisplayProps) {
  const count = total ?? sentences.length

  return (
    <div className="bg-white rounded-xl shadow-md p-2 space-y-1">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900 text-xs">
          {heading} {targetWord && <span className="text-gray-500 font-normal">— {targetWord}</span>}
        </h4>
        <span className="text-[10px] text-gray-500">
          {sentences.length < count ? `${sentences.length} of ${count}` : count}
        </span>
      </div>

      {/* Sentence List */}
      {sentences.length > 0 ? (
        <div className="space-y-0.5 max-h-[75vh] overflow-y-auto">
          {sentences.map((sentence, i) => {
            const color = sentence.label && primaryValues.length > 0
              ? getNodeColor({ [sentence.label]: 1 }, primaryValues, gradient)
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
              <div key={sentence.probe_id || i} className="bg-gray-50 rounded px-1.5 py-1">
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
          {isLoading ? 'Loading…' : 'No sentences'}
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
