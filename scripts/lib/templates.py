"""
Handlebars-style template engine using Python stdlib only.
Supports {{variable}}, {{#if}}, {{#each}}, and {{#unless}} blocks.
"""

import re
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "templates"


def _resolve_var(name, context):
    """Resolve dotted variable name from context dict."""
    parts = name.strip().split(".")
    val = context
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p)
        else:
            return None
        if val is None:
            return None
    return val


def render(template_str, context):
    """Render a Handlebars-style template string with the given context."""
    result = template_str

    # Process {{#each items}} ... {{/each}} blocks
    each_pattern = re.compile(
        r"\{\{#each\s+([\w.]+)\}\}(.*?)\{\{/each\}\}", re.DOTALL
    )
    while each_pattern.search(result):
        def replace_each(m):
            list_name = m.group(1)
            body = m.group(2)
            items = _resolve_var(list_name, context)
            if not items or not isinstance(items, list):
                return ""
            output = []
            for item in items:
                if isinstance(item, dict):
                    rendered = render(body, {**context, **item, "this": item})
                else:
                    rendered = render(body, {**context, "this": str(item)})
                output.append(rendered)
            return "".join(output)
        result = each_pattern.sub(replace_each, result)

    # Process {{#if var}} ... {{else}} ... {{/if}} blocks
    if_else_pattern = re.compile(
        r"\{\{#if\s+([\w.]+)\}\}(.*?)\{\{else\}\}(.*?)\{\{/if\}\}", re.DOTALL
    )
    while if_else_pattern.search(result):
        def replace_if_else(m):
            var_name = m.group(1)
            true_block = m.group(2)
            false_block = m.group(3)
            val = _resolve_var(var_name, context)
            if val and val != "none" and val is not False:
                return render(true_block, context)
            return render(false_block, context)
        result = if_else_pattern.sub(replace_if_else, result)

    # Process {{#if var}} ... {{/if}} blocks (no else)
    if_pattern = re.compile(
        r"\{\{#if\s+([\w.]+)\}\}(.*?)\{\{/if\}\}", re.DOTALL
    )
    while if_pattern.search(result):
        def replace_if(m):
            var_name = m.group(1)
            body = m.group(2)
            val = _resolve_var(var_name, context)
            if val and val != "none" and val is not False:
                return render(body, context)
            return ""
        result = if_pattern.sub(replace_if, result)

    # Process {{#unless var}} ... {{/unless}} blocks
    unless_pattern = re.compile(
        r"\{\{#unless\s+([\w.]+)\}\}(.*?)\{\{/unless\}\}", re.DOTALL
    )
    while unless_pattern.search(result):
        def replace_unless(m):
            var_name = m.group(1)
            body = m.group(2)
            val = _resolve_var(var_name, context)
            if not val or val == "none" or val is False:
                return render(body, context)
            return ""
        result = unless_pattern.sub(replace_unless, result)

    # Replace simple {{variable}} tokens
    def replace_var(m):
        var_name = m.group(1).strip()
        val = _resolve_var(var_name, context)
        if val is None:
            return ""
        if isinstance(val, list):
            return ", ".join(str(v) for v in val)
        return str(val)

    result = re.sub(r"\{\{([\w.]+)\}\}", replace_var, result)

    return result


def load_template(name):
    """Load a template file from the assets/templates directory."""
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(name, context):
    """Load and render a template by name."""
    template_str = load_template(name)
    return render(template_str, context)
