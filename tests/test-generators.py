#!/usr/bin/env python3
"""
Unit tests for all generators.
Tests template rendering, soul generation, user generation,
identity generation, and memory infrastructure generation.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from lib.templates import render, render_template, load_template
from lib.providers import (
    get_voice_provider_config,
    get_image_provider_config,
    VOICE_PRESETS,
)
from lib.config import _deep_merge, _strip_secrets

# Import generators
from importlib.machinery import SourceFileLoader

generate_soul = SourceFileLoader(
    "generate_soul",
    str(Path(__file__).resolve().parent.parent / "scripts" / "generate-soul.py"),
).load_module()

generate_user = SourceFileLoader(
    "generate_user",
    str(Path(__file__).resolve().parent.parent / "scripts" / "generate-user.py"),
).load_module()

generate_identity = SourceFileLoader(
    "generate_identity",
    str(Path(__file__).resolve().parent.parent / "scripts" / "generate-identity.py"),
).load_module()

generate_memory = SourceFileLoader(
    "generate_memory",
    str(Path(__file__).resolve().parent.parent / "scripts" / "generate-memory.py"),
).load_module()


class TestTemplateEngine(unittest.TestCase):
    """Test the Handlebars-style template engine."""

    def test_simple_variable(self):
        result = render("Hello {{name}}!", {"name": "Pepper"})
        self.assertEqual(result, "Hello Pepper!")

    def test_missing_variable(self):
        result = render("Hello {{name}}!", {})
        self.assertEqual(result, "Hello !")

    def test_dotted_variable(self):
        result = render("{{user.name}}", {"user": {"name": "Chance"}})
        self.assertEqual(result, "Chance")

    def test_if_block_true(self):
        result = render("{{#if show}}visible{{/if}}", {"show": True})
        self.assertEqual(result, "visible")

    def test_if_block_false(self):
        result = render("{{#if show}}visible{{/if}}", {"show": False})
        self.assertEqual(result, "")

    def test_if_else_block(self):
        template = "{{#if show}}yes{{else}}no{{/if}}"
        self.assertEqual(render(template, {"show": True}), "yes")
        self.assertEqual(render(template, {"show": False}), "no")

    def test_unless_block(self):
        template = "{{#unless hide}}visible{{/unless}}"
        self.assertEqual(render(template, {"hide": False}), "visible")
        self.assertEqual(render(template, {"hide": True}), "")

    def test_each_block_strings(self):
        template = "{{#each items}}[{{this}}]{{/each}}"
        result = render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "[a][b][c]")

    def test_each_block_empty(self):
        template = "{{#each items}}[{{this}}]{{/each}}"
        result = render(template, {"items": []})
        self.assertEqual(result, "")

    def test_list_variable(self):
        result = render("{{items}}", {"items": ["a", "b", "c"]})
        self.assertEqual(result, "a, b, c")

    def test_nested_if_in_each(self):
        template = "{{#each items}}{{#if this}}+{{/if}}{{/each}}"
        # "this" is the item itself; strings are truthy
        result = render(template, {"items": ["a", "b"]})
        self.assertEqual(result, "++")

    def test_load_template(self):
        """Ensure all template files exist and load."""
        for name in ["SOUL.md.hbs", "USER.md.hbs", "IDENTITY.md.hbs",
                      "MEMORY.md.hbs", "HEARTBEAT.md.hbs", "AGENTS.md.hbs"]:
            content = load_template(name)
            self.assertTrue(len(content) > 0, f"Template {name} is empty")


class TestProviders(unittest.TestCase):
    """Test provider configuration builders."""

    def test_elevenlabs_config(self):
        config = get_voice_provider_config("elevenlabs", voice_id="abc123")
        self.assertEqual(config["provider"], "elevenlabs")
        self.assertEqual(config["elevenlabs"]["voiceId"], "abc123")
        self.assertEqual(config["elevenlabs"]["modelId"], "eleven_v3")

    def test_grok_tts_config(self):
        config = get_voice_provider_config("grok")
        self.assertEqual(config["provider"], "grok")
        self.assertEqual(config["grok"]["modelId"], "grok-3-tts")

    def test_builtin_config(self):
        config = get_voice_provider_config("builtin", voice="alloy")
        self.assertEqual(config["provider"], "builtin")
        self.assertEqual(config["builtin"]["voice"], "alloy")

    def test_none_voice(self):
        config = get_voice_provider_config("none")
        self.assertIsNone(config)

    def test_unknown_voice_provider(self):
        with self.assertRaises(ValueError):
            get_voice_provider_config("unknown")

    def test_gemini_image_config(self):
        config = get_image_provider_config("gemini", description="test desc")
        self.assertEqual(config["provider"], "gemini")
        self.assertEqual(config["canonicalLook"]["description"], "test desc")

    def test_both_image_config(self):
        config = get_image_provider_config("both", description="test")
        self.assertEqual(config["provider"], "gemini")
        self.assertIn("grok", config)

    def test_none_image(self):
        config = get_image_provider_config("none")
        self.assertIsNone(config)

    def test_voice_presets_exist(self):
        for key in ["default", "intimate", "excited", "professional"]:
            self.assertIn(key, VOICE_PRESETS)


class TestConfig(unittest.TestCase):
    """Test config helpers."""

    def test_deep_merge(self):
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"c": 99, "e": 5}, "f": 6}
        result = _deep_merge(base, override)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 99)
        self.assertEqual(result["b"]["d"], 3)
        self.assertEqual(result["b"]["e"], 5)
        self.assertEqual(result["f"], 6)

    def test_strip_secrets(self):
        d = {"apiKey": "secret", "name": "test", "nested": {"token": "xyz", "value": 1}}
        _strip_secrets(d)
        self.assertNotIn("apiKey", d)
        self.assertIn("name", d)
        self.assertNotIn("token", d["nested"])
        self.assertIn("value", d["nested"])


class TestGenerateSoul(unittest.TestCase):
    """Test SOUL.md generation."""

    def _load_profile(self, archetype):
        profiles_dir = Path(__file__).resolve().parent.parent / "assets" / "personality-profiles"
        with open(profiles_dir / f"{archetype}.json", "r") as f:
            return json.load(f)

    def test_professional_soul(self):
        profile = self._load_profile("professional")
        profile["name"] = "Atlas"
        profile["emoji"] = "🏛️"
        result = generate_soul.generate_soul(profile)
        self.assertIn("Atlas", result)
        self.assertIn("🏛️", result)
        self.assertIn("SOUL.md", result)
        self.assertIn("Core Truths", result)
        self.assertIn("Communication", result)
        self.assertIn("Continuity", result)
        # Professional should not have flirtation
        self.assertNotIn("Flirtation is welcome", result)

    def test_companion_soul(self):
        profile = self._load_profile("companion")
        profile["name"] = "Pepper"
        profile["emoji"] = "🌶️"
        profile["userName"] = "Chance"
        profile["userRelationship"] = {"userName": "Chance"}
        result = generate_soul.generate_soul(profile)
        self.assertIn("Pepper", result)
        self.assertIn("🌶️", result)
        self.assertIn("Flirtation is welcome", result)
        self.assertIn("Pet names", result)

    def test_deterministic_output(self):
        """Same input always produces same output."""
        profile = self._load_profile("mentor")
        profile["name"] = "Sage"
        profile["emoji"] = "📚"
        result1 = generate_soul.generate_soul(profile)
        result2 = generate_soul.generate_soul(profile)
        self.assertEqual(result1, result2)

    def test_all_archetypes_generate(self):
        """All archetype profiles generate valid SOUL.md."""
        for arch in ["professional", "companion", "creative", "mentor", "custom"]:
            profile = self._load_profile(arch)
            profile["name"] = "Test"
            profile["emoji"] = "🧪"
            result = generate_soul.generate_soul(profile)
            self.assertIn("SOUL.md", result)
            self.assertIn("Test", result)
            self.assertIn("Continuity", result)


class TestGenerateUser(unittest.TestCase):
    """Test USER.md generation."""

    def test_basic_user(self):
        context = {
            "userName": "Chance",
            "callNames": "Chance, babe",
            "timezone": "America/New_York",
        }
        result = generate_user.generate_user(context)
        self.assertIn("Chance", result)
        self.assertIn("babe", result)
        self.assertIn("America/New_York", result)

    def test_user_with_notes(self):
        context = {
            "userName": "Chance",
            "callNames": "Chance",
            "timezone": "UTC",
            "userNotes": "Loves coffee.",
        }
        result = generate_user.generate_user(context)
        self.assertIn("Loves coffee", result)

    def test_user_with_pronouns(self):
        context = {
            "userName": "Alex",
            "callNames": "Alex",
            "timezone": "UTC",
            "pronouns": "they/them",
        }
        result = generate_user.generate_user(context)
        self.assertIn("they/them", result)


class TestGenerateIdentity(unittest.TestCase):
    """Test IDENTITY.md generation."""

    def test_basic_identity(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Executive assistant",
            "vibe": "Calm and competent",
        }
        result = generate_identity.generate_identity(context)
        self.assertIn("Pepper", result)
        self.assertIn("🌶️", result)
        self.assertIn("Executive assistant", result)

    def test_identity_with_nickname(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Assistant",
            "vibe": "Cool",
            "nickname": "Pep",
        }
        result = generate_identity.generate_identity(context)
        self.assertIn("Pep", result)


class TestGenerateMemory(unittest.TestCase):
    """Test memory infrastructure generation."""

    def setUp(self):
        self.workspace = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def test_generates_all_files(self):
        context = {
            "name": "Pepper",
            "emoji": "🌶️",
            "creature": "Assistant",
            "userName": "Chance",
            "createdDate": "2026-03-29",
            "dailyNotes": True,
            "longTermCuration": True,
            "heartbeatMaintenance": True,
        }
        # Generate each file
        memory_content = generate_memory.generate_memory(context)
        self.assertIn("Pepper", memory_content)
        self.assertIn("2026-03-29", memory_content)

        heartbeat_content = generate_memory.generate_heartbeat(context)
        self.assertIn("MEMORY.md", heartbeat_content)

        agents_context = dict(context)
        agents_context["platformNotes"] = []
        agents_content = generate_memory.generate_agents(agents_context)
        self.assertIn("Pepper", agents_content)

    def test_daily_note_creation(self):
        note_path = generate_memory.create_daily_note(
            self.workspace, "Pepper", "🌶️", "2026-03-29"
        )
        self.assertTrue(Path(note_path).exists())
        content = Path(note_path).read_text()
        self.assertIn("Persona created", content)
        self.assertIn("2026-03-29", content)

    def test_memory_dir_created(self):
        generate_memory.create_daily_note(self.workspace, "Test", "🧪", "2026-03-29")
        self.assertTrue((Path(self.workspace) / "memory").is_dir())


if __name__ == "__main__":
    unittest.main()
