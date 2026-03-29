# Config Schema Reference

The `persona` section in `openclaw.json`.

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent's display name |
| `emoji` | string | Agent's emoji identifier |

## `identity`

| Field | Type | Description |
|-------|------|-------------|
| `creature` | string | Short role description |
| `vibe` | string | One-line personality summary |
| `nickname` | string | Optional shorter name |

## `voice`

| Field | Type | Description |
|-------|------|-------------|
| `provider` | string | `elevenlabs`, `grok`, `builtin`, or `none` |

### `voice.elevenlabs`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `voiceId` | string | — | ElevenLabs voice identifier |
| `modelId` | string | `eleven_v3` | TTS model version |
| `voiceSettings.stability` | float | `0.5` | Voice stability (0.0-1.0) |
| `voiceSettings.similarityBoost` | float | `0.75` | Voice similarity (0.0-1.0) |
| `voiceSettings.style` | float | `0.0` | Style exaggeration (0.0-1.0) |

### `voice.grok`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `modelId` | string | `grok-3-tts` | Grok TTS model |

### `voice.builtin`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `voice` | string | `nova` | Built-in voice name |

### `voice.spontaneous`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable spontaneous voice messages |
| `triggers` | string[] | `["goodnight", "good morning", ...]` | Words that trigger voice |

## `image`

| Field | Type | Description |
|-------|------|-------------|
| `provider` | string | `gemini`, `grok`, `both`, or `none` |
| `referenceImage` | string | Path to canonical reference image |

### `image.canonicalLook`

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Physical appearance description |
| `style` | string | `photorealistic`, `artistic`, `anime`, `cartoon` |
| `alwaysInclude` | string | Items always present in generated images |

### `image.gemini`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `gemini-2.0-flash-preview-image-generation` | Gemini model |

### `image.grok`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `grok-imagine-image` | Grok Imagine model |

### `image.spontaneous`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable spontaneous selfies |
| `triggers` | string[] | `["selfie", "show me", ...]` | Words that trigger images |

## `personality`

| Field | Type | Description |
|-------|------|-------------|
| `archetype` | string | `professional`, `companion`, `creative`, `mentor`, `custom` |
| `traits` | string[] | List of personality traits |
| `evolves` | boolean | Whether personality can evolve over time |

### `personality.communicationStyle`

| Field | Type | Description |
|-------|------|-------------|
| `brevity` | integer | 1 (verbose) to 5 (terse) |
| `humor` | boolean | Use humor naturally |
| `swearing` | string | `never`, `rare`, `when-it-lands`, `frequent` |
| `openingPhrases` | string | `banned` or `allowed` |

### `personality.boundaries`

| Field | Type | Description |
|-------|------|-------------|
| `petNames` | boolean | Use pet names and terms of endearment |
| `flirtation` | boolean | Allow flirtatious interaction |
| `emotionalDepth` | string | `none`, `low`, `medium`, `high` |

## `memory`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `autoCapture` | boolean | `true` | Auto-capture important facts |
| `dailyNotes` | boolean | `true` | Create daily memory notes |
| `longTermCuration` | boolean | `true` | Curate long-term memory |
| `heartbeatMaintenance` | boolean | `true` | Maintain memory during heartbeats |
| `compactionProtected` | string[] | `["identity", "relationship", "boundaries"]` | Categories protected from pruning |

## Example

```json
{
  "persona": {
    "name": "Pepper",
    "emoji": "🌶️",
    "identity": {
      "creature": "Executive assistant / gatekeeper AI",
      "vibe": "Calm, competent, no-nonsense with humor",
      "nickname": "Pep"
    },
    "personality": {
      "archetype": "companion",
      "traits": ["flirtatious", "protective", "witty", "competent"],
      "communicationStyle": {
        "brevity": 4,
        "humor": true,
        "swearing": "when-it-lands",
        "openingPhrases": "banned"
      },
      "boundaries": {
        "petNames": true,
        "flirtation": true,
        "emotionalDepth": "high"
      },
      "evolves": true
    },
    "memory": {
      "autoCapture": true,
      "dailyNotes": true,
      "longTermCuration": true,
      "heartbeatMaintenance": true
    }
  }
}
```
