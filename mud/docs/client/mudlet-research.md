# Mudlet for MUD Operators — Research

**Status:** research in progress (findings pass pending).
**Lens:** how people *running* MUDs use Mudlet — the server-side / operator integration surface —
**not** a player how-to. The goal is to know exactly what leverage Mudlet gives a MUD server so we can
decide what Whiteout should light up (see the companion `mudlet-brainstorm.md`).

Whiteout runs on **Evennia 6.0**, so a recurring question in each section is: *what does Evennia already
expose, and what would we have to send ourselves?*

---

## 1. What Mudlet is, and why an operator cares
_(Cross-platform Lua-scriptable MUD client; the leverage is the out-of-band protocol + mapper + GUI/package
system a server can drive. To fill.)_

## 2. The server→client protocol stack (the real leverage)
- **Telnet option negotiation** — the handshake underneath everything.
- **GMCP** (Generic MUD Communication Protocol) — the primary structured-data channel; modules, format.
- **MSDP** — the alternative/complementary structured channel.
- **MXP** — clickable/rich text (`<send>`, spans, links, images).
- **MCCP** (compression), **MSSP** (server listing for crawlers), **MSP/MCMP** (sound), **NAWS**,
  **TTYPE/MTTS** (client feature flags), charset/UTF-8.
_(To fill with formats, examples, and what the server must emit.)_

## 3. The Mudlet mapper (server-fed mapping)
- How the automapper works; the `Room.Info` GMCP message; vnums, areas, exits, coordinates, environments.
- The Generic Mapper script; custom/special exits; room user-data; shipping a prebuilt map.
_(To fill.)_

## 4. The Mudlet GUI / package system
- **Geyser** UI framework; gauges, labels, miniConsoles/user windows, adjustable containers, buttons.
- **Packages** — `.mpackage`/XML, the `muddler` build tool, versioning, distribution.
- **Auto-install from the server** — pointing Mudlet at a downloadable GUI package + version check; the
  package manager / online repository.
- **Discord Rich Presence** via GMCP.
_(To fill.)_

## 5. Scripting model operators must understand
- Lua; triggers/aliases/keys/timers; the event system; GMCP event handlers; how packages register handlers.
_(To fill.)_

## 6. Sound, atmosphere, accessibility
_(MSP/MCMP sound; MXP + screen-reader accessibility. To fill.)_

## 7. How Evennia exposes all this
_(GMCP/MSDP/OOB, MXP, MSSP, MCCP, TTYPE; the concrete API to emit GMCP from Evennia. To fill.)_

## 8. Who does this well (exemplar MUDs & packages)
_(IRE games etc. and what their packages do. To fill.)_

## 9. Key takeaways for Whiteout
_(Bridge into the brainstorm doc. To fill.)_

## Sources
_(URLs collected during the research pass.)_
