#!/usr/bin/env python3
"""Re-inject the working constitution + skill inventory FRESH each turn, so they don't lose force as
the context window fills (a rule loaded once at the top gets buried over a long session). Wired to
SessionStart / UserPromptSubmit / SubagentStart (always) and PreToolUse before file edits (throttled,
for long autonomous runs where no user prompt fires to refresh it). Safe no-op if files are missing."""
import sys, json, os, time

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
event = data.get("hook_event_name", "SessionStart")
root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
stamp = os.path.join(root, ".claude", "hooks", ".inject-stamp")

# Throttle the PreToolUse firing so a long run doesn't re-inject before every single edit.
if event == "PreToolUse":
    try:
        if time.time() - os.path.getmtime(stamp) < 300:      # < 5 min since last injection
            sys.exit(0)
    except OSError:
        pass

parts = []
try:
    with open(os.path.join(root, ".claude", "agent-constitution.md")) as f:
        parts.append(f.read().strip())
except OSError:
    pass

# skill inventory: name + one-line description from each SKILL.md frontmatter
inv = []
skills_dir = os.path.join(root, ".claude", "skills")
try:
    for name in sorted(os.listdir(skills_dir)):
        skfile = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(skfile):
            continue
        desc, in_fm, seen_open = "", False, False
        with open(skfile) as f:
            for line in f:
                s = line.strip()
                if s == "---":
                    if not seen_open:
                        seen_open, in_fm = True, True
                        continue
                    break                                    # end of frontmatter
                if in_fm and s.startswith("description:"):
                    desc = s.split("description:", 1)[1].strip().strip('"').strip("'")
        inv.append(f"  - {name}: {desc[:180]}")
except OSError:
    pass
if inv:
    parts.append("Available skills (invoke the matching one with the Skill tool before hand-rolling):\n"
                 + "\n".join(inv))

text = "\n\n".join(p for p in parts if p)
if text:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))
    try:
        open(stamp, "a").close()
        os.utime(stamp, None)
    except OSError:
        pass
