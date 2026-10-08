import { BrowserRouter as Router, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import MUDApp from './pages/MUDApp'
import LayersWorkspace from './pages/LayersWorkspace'
import BuildWorkspace from './pages/BuildWorkspace'
import './App.css'

// Any other address opens Layers, keeping the view it names
function ToLayers() {
  const { search } = useLocation()
  return <Navigate to={`/layers${search}`} replace />
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MUDApp />}>
          <Route index element={<ToLayers />} />
          <Route path="layers" element={<LayersWorkspace />} />
          <Route path="build" element={<BuildWorkspace />} />
          <Route path="*" element={<ToLayers />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
