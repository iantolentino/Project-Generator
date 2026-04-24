"""
prompts.py – Interactive CLI questionnaire (questionary-based).
"""

import questionary
from project_gen.stacks import CATEGORY_STACK_MAP, STACK_META, resolve_stack

PLATFORMS = ["Web", "Desktop", "Hybrid"]

CATEGORIES = [
    "E-commerce", "SaaS product", "Business dashboard", "Blogging platform",
    "AI chatbot interface", "Streaming platform", "Social media app",
    "Video conferencing", "Cryptocurrency tracker", "Gaming hub",
    "Ticketing system", "Learning management system", "Healthcare management",
    "Event management", "Travel booking", "Restaurant ordering system",
    "Finance tracker", "Inventory management", "Portfolio site", "Music player",
]

STYLES = ["Modern", "Minimal", "Dark Theme", "Corporate", "Playful", "Elegant"]
SCOPES = ["Scalable app", "Landing page", "Static-only"]


def gather_project_options() -> dict:
    platform = questionary.select(
        "1️⃣  Select platform:",
        choices=PLATFORMS
    ).ask()

    category = questionary.select(
        "2️⃣  Choose project category:",
        choices=CATEGORIES
    ).ask()

    # Show suggested stack
    stack_id = resolve_stack(platform, category)
    meta = STACK_META.get(stack_id, {})
    if meta:
        questionary.print(
            f"\n   💡 Suggested stack: {meta['label']}",
            style="fg:ansigreen"
        )
        questionary.print(
            f"   🏷  Tags: {', '.join(meta.get('tags', []))}",
            style="fg:ansicyan"
        )

    colors = questionary.text(
        "\n3️⃣  Primary brand color (hex or name):",
        default="#3B82F6"
    ).ask()

    style = questionary.select(
        "4️⃣  Design style:",
        choices=STYLES
    ).ask()

    scope = questionary.select(
        "5️⃣  Project scope:",
        choices=SCOPES
    ).ask()

    project_name = questionary.text(
        "6️⃣  Project name (used as folder name):",
        default="my-project"
    ).ask()

    return {
        "platform": platform,
        "category": category,
        "colors": [colors.strip()],
        "style": style,
        "scope": scope,
        "project_name": project_name,
    }
