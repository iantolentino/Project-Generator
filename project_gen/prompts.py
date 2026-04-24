import questionary

PLATFORMS = ["Web", "Desktop", "Hybrid"]
CATEGORIES = [
    "E-commerce", "Streaming platform", "Ticketing system",
    "Business dashboard", "Blogging platform", "Portfolio site",
    "Social media app", "Learning management system", "SaaS product",
    "Cryptocurrency tracker", "AI chatbot interface", "Healthcare management",
    "Restaurant ordering system", "Event management", "Travel booking",
    "Music player", "Video conferencing", "Inventory management",
    "Finance tracker", "Gaming hub"
]
STYLES = ["Modern", "Minimal", "Dark Theme", "Corporate", "Playful", "Elegant"]
SCOPES = ["Scalable app", "Landing page", "Static-only"]

def gather_project_options():
    platform = questionary.select(
        "1. Select platform:",
        choices=PLATFORMS
    ).ask()

    category = questionary.select(
        "2. Choose project category:",
        choices=CATEGORIES
    ).ask()

    colors = questionary.text(
        "3. Pick up to 5 colors (comma-separated hex or names):",
        default="#3B82F6,#10B981,#F59E0B,#EF4444,#8B5CF6"
    ).ask()
    colors_list = [c.strip() for c in colors.split(",") if c.strip()][:5]

    style = questionary.select(
        "4. Design style:",
        choices=STYLES
    ).ask()

    scope = questionary.select(
        "5. Project scope:",
        choices=SCOPES
    ).ask()

    return {
        "platform": platform,
        "category": category,
        "colors": colors_list,
        "style": style,
        "scope": scope
    }