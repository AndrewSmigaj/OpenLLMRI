/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** The MUD's websocket port on the host (the repo root's .env) */
  readonly MUD_WS_PORT?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
