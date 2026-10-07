import { Component, type ErrorInfo, type ReactNode } from 'react'

interface PanelErrorBoundaryProps {
  /** The panel's name, shown if it fails */
  name: string
  children: ReactNode
}

interface PanelErrorBoundaryState {
  error: Error | null
}

/**
 * Keeps one panel's rendering fault from blanking the whole page: the failed panel shows its error
 * and the others keep working. Give the boundary a `key` that changes with the panel's inputs
 * (session, clustering) so a new selection tries the panel again.
 */
export default class PanelErrorBoundary extends Component<PanelErrorBoundaryProps, PanelErrorBoundaryState> {
  state: PanelErrorBoundaryState = { error: null }

  static getDerivedStateFromError(error: Error): PanelErrorBoundaryState {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error(`${this.props.name} panel failed:`, error, info.componentStack)
  }

  render() {
    if (this.state.error) {
      return (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-xs text-red-800">
          <p className="font-semibold">{this.props.name} couldn't be shown.</p>
          <p className="font-mono mt-1 break-words">{this.state.error.message}</p>
        </div>
      )
    }
    return this.props.children
  }
}
