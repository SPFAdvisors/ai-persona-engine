# AI Persona Engine

**Skill Name:** ai-persona-engine
**Version:** 1.0
**Author:** SPFAdvisors

Create a fully realized AI persona — voice, face, personality, and memory — in under 5 minutes.

---

## Quick Start

```bash
# Install from ClawHub
clawhub install ai-persona-engine

# Create your first persona
openclaw persona create

# That's it. The wizard handles everything.
```

---

## Commands

### `persona create`

Interactive wizard that walks through persona creation step by step.

```bash
openclaw persona create
```

The wizard covers 7 steps:

1. **Name & Identity** — name, emoji, description, nickname
2. **Personality** — archetype selection, communication style, relationship boundaries
3. **Voice** — provider selection (ElevenLabs, Grok TTS, built-in), voice testing
4. **Visual Identity** — appearance description, reference image generation
5. **Your Context** — USER.md with your name, timezone, preferences
6. **Memory** — daily notes, long-term curation, heartbeat maintenance
7. **Platforms** — channel selection and per-channel behavior

Output: SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, and updated openclaw.json.

### `persona update`

Modify specific persona fields without re-running the full wizard.

```bash
# Update voice provider
openclaw persona update --voice-provider elevenlabs --voice-id abc123

# Add or remove personality traits
openclaw persona update --add-trait "sarcastic" --remove-trait "formal"

# Update appearance and regenerate reference image
openclaw persona update --appearance "new description..." --regen-image

# Regenerate SOUL.md from current config
openclaw persona update --regen-soul

# Interactive mode (step-by-step, choose what to change)
openclaw persona update -i
```

### `persona export`

Package the persona into a portable `.persona` bundle.

```bash
# Basic export (no memory, no API keys)
openclaw persona export

# Include memory files
openclaw persona export --name pepper-backup --include-memory

# Include voice config (still excludes API keys)
openclaw persona export --include-voice-config
```

### `persona import`

Import a `.persona` bundle into a workspace.

```bash
# Interactive import (confirms each file)
openclaw persona import pepper.persona

# Import into a specific workspace
openclaw persona import pepper.persona --workspace ~/.openclaw/workspace-new

# Overwrite existing files without prompting
openclaw persona import pepper.persona --force
```

---

## File Structure

```
ai-persona-engine/
├── SKILL.md                     # This file
├── DESIGN.md                    # Full design document
├── scripts/
│   ├── persona-create.sh        # Setup wizard
│   ├── persona-update.sh        # Field updater
│   ├── persona-export.sh        # Bundle exporter
│   ├── persona-import.sh        # Bundle importer
│   ├── generate-soul.py         # SOUL.md generator
│   ├── generate-user.py         # USER.md generator
│   ├── generate-identity.py     # IDENTITY.md generator
│   ├── generate-memory.py       # MEMORY.md + memory/ scaffolding
│   ├── voice-setup.py           # Voice provider config + testing
│   ├── image-setup.py           # Image provider config + reference image
│   └── lib/
│       ├── providers.py         # Provider abstraction layer
│       ├── templates.py         # File templates and defaults
│       ├── config.py            # openclaw.json helpers
│       └── prompts.py           # Wizard prompt definitions
├── references/
│   ├── voice-providers.md       # Voice provider setup guide
│   ├── image-providers.md       # Image provider setup guide
│   ├── personality-archetypes.md # Archetype reference
│   ├── soul-writing-guide.md    # SOUL.md writing tips
│   └── config-schema.md         # openclaw.json schema reference
├── assets/
│   ├── personality-profiles/    # JSON presets per archetype
│   └── templates/               # Handlebars templates for generated files
└── tests/
    ├── test-wizard.sh
    ├── test-voice.sh
    ├── test-image.sh
    ├── test-export-import.sh
    └── test-generators.py
```

---

## Configuration

The persona engine adds a `persona` section to `openclaw.json`. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `persona.name` | string | Agent's display name |
| `persona.emoji` | string | Agent's emoji identifier |
| `persona.identity` | object | Creature type, vibe, nickname |
| `persona.voice` | object | Voice provider and settings |
| `persona.image` | object | Image provider and canonical look |
| `persona.personality` | object | Archetype, traits, communication style |
| `persona.memory` | object | Memory capture and curation settings |

See [references/config-schema.md](references/config-schema.md) for the full schema.

---

## Dependencies

**Required:**
- OpenClaw (any version with skill support)
- Python 3.9+
- Node.js 22+

**Optional (based on chosen providers):**
- ElevenLabs API key (voice)
- Gemini API key (image generation)
- xAI API key (Grok TTS / Grok Imagine)
- ffmpeg (audio format conversion for WhatsApp voice messages)

---

## Further Reading

- [Voice Providers Guide](references/voice-providers.md)
- [Image Providers Guide](references/image-providers.md)
- [Personality Archetypes](references/personality-archetypes.md)
- [SOUL.md Writing Guide](references/soul-writing-guide.md)
- [Config Schema Reference](references/config-schema.md)
- [Design Document](DESIGN.md)
