import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import questionary
from project_gen.utils import init_git_repo, write_file

CATEGORY_STACK = {
    "Web": {
        "E-commerce": ("Next.js", "PostgreSQL", "Prisma"),
        "Streaming platform": ("React + Node.js", "MongoDB", "Mongoose"),
        "Social media app": ("Django", "PostgreSQL", "Django ORM"),
        "default": ("React", "SQLite", "None")
    },
    "Desktop": {
        "default": ("Electron", "SQLite", "Sequelize")
    },
    "Hybrid": {
        "default": ("Tauri", "SQLite", "Diesel")
    }
}

def suggest_stack(platform, category):
    platform_map = CATEGORY_STACK.get(platform, {})
    return platform_map.get(category, platform_map.get("default", ("React", "SQLite", "None")))

def generate_project(options):
    print("\n⏳ Generating project...\n")
    
    project_name = questionary.text("Project name:", default="my-project").ask()
    target_dir = Path.cwd() / project_name
    target_dir.mkdir(exist_ok=True)
    print(f"✅ Created directory: {target_dir}")
    
    framework, database, orm = suggest_stack(options["platform"], options["category"])
    print(f"📦 Selected stack: {framework} + {database}")
    
    context = {
        "project_name": project_name,
        "platform": options["platform"],
        "category": options["category"],
        "colors": options["colors"],
        "style": options["style"],
        "scope": options["scope"],
        "framework": framework,
        "database": database,
        "orm": orm,
    }
    
    template_dir = Path(__file__).parent / "templates" / options["platform"].lower()
    if not template_dir.exists():
        print(f"⚠️  No templates found for platform '{options['platform']}'. Using fallback 'web'.")
        template_dir = Path(__file__).parent / "templates" / "web"
    
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    # Recursive function using Path objects
    def render_directory(current_template_path: Path, relative_path: Path = Path(".")):
        for item in current_template_path.iterdir():
            if item.is_dir():
                render_directory(item, relative_path / item.name)
            else:
                output_filename = item.name[:-3] if item.name.endswith('.j2') else item.name
                output_path = target_dir / relative_path / output_filename
                
                if item.name.endswith('.j2'):
                    # Template path relative to template_dir
                    template_rel_path = str((relative_path / item.name).as_posix())
                    template = env.get_template(template_rel_path)
                    content = template.render(context)
                    write_file(output_path, content)
                    print(f"📄 Rendered: {output_filename}")
                else:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(item, output_path)
                    print(f"📄 Copied: {output_filename}")
    
    render_directory(template_dir)
    
    init_git_repo(target_dir)
    print("🔧 Initialized git repository")
    
    print(f"\n✨ Project ready at: {target_dir}")