# Open LLMRI — Frontend

React + Vite + TypeScript app for reading lenses on gpt-oss-20b's internal states: cluster and
expert flows over every layer, validation, node details and LLM-written reports, with the MUD's
terminal docked below. The shell (`MUDApp.tsx`) holds two workspaces, Layers (`/layers`) and Build
(`/build`).

## Layout

```
src/
├── App.tsx, main.tsx            # The routes: the shell with /layers and /build
├── pages/
│   ├── MUDApp.tsx               # The shell: top bar, a workspace, the MUD terminal's dock, the event stream
│   ├── LayersWorkspace.tsx      # Layers: both charts over every layer, the details panel, the lower tabs
│   └── BuildWorkspace.tsx       # Build: the lens form, mass-mean lenses, validation, versions, reports
├── components/
│   ├── shell/                   # TopBar, JobsMenu, TerminalDock, the shell's context
│   ├── layers/                  # LayerCharts, LayerStrip, colour controls and legend, DetailsPanel,
│   │                            #   NodeDetails, FingerprintPanel, LowerTabs, LegacyReports
│   ├── lenses/                  # LensForm, LensVersions, LensBadges, LensValidation, LensReport,
│   │                            #   AnalystStatus, the mass-mean form, results and details, JobProgress
│   ├── analysis/                # AnalysisReport, CardBody, CardQuestions, CitedText (the LLM cards);
│   │                            #   ContextSensitiveCard, SchemaSummary, WindowAnalysis
│   ├── charts/                  # AllLayerSankeyView, SankeyChart, SteppedTrajectoryPlot (3-D)
│   ├── common/                  # ExportMenu, PanelErrorBoundary, Tokens
│   └── terminal/MUDTerminal.tsx # The embedded MUD client
├── hooks/                       # The view state (in the URL), lens flows, context, details, marks and
│                                #   members, cards, jobs, the event stream, the MUD connection
├── color/                       # OKLab mixing, colour schemes and the legend (unit-tested)
├── api/client.ts                # The typed API client
├── types/                       # Its types (lens, cards, api, evennia)
└── utils/                       # Selections and card ids, layer geometry, exports with recipes, lab presets
```

## Running

```bash
npm ci
npm run dev     # http://localhost:5173
npm run lint && npx tsc -b && npm run test && npm run build   # what CI runs
```

The backend is expected at `http://localhost:8000/api`, and only accepts browser calls from the
app's origin (`APP_ORIGINS` in the root `.env`).

WSL2 note: `vite.config.ts` enables `usePolling: true` for file watching, so changes appear
without a refresh.

## Conventions

- **The view's state lives in the URL** (capture, lens, layer, zoom, colours, rank, selection,
  tab), so links, commands and exported figures share it.
- **The app listens to the backend's event stream:** `show` commands open a view, `job` events
  keep jobs current, `lens` events make views re-read what changed. Nothing polls while it's open.
- **Every chart exports** its picture and its data, each carrying its recipe.
- **Visitors read only;** a lab room in the MUD locks the capture it shows.
