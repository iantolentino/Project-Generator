import os
import shutil
import time
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import questionary
from project_gen.utils import init_git_repo, write_file
from project_gen.structure_maker import parse_tree_structure, STRUCTURE_TEMPLATES

CATEGORY_STACK = {
    "Web": {
        "E-commerce": ("Next.js", "PostgreSQL", "Prisma"),
        "Streaming platform": ("React + Node.js", "MongoDB", "Mongoose"),
        "Social media app": ("Django", "PostgreSQL", "Django ORM"),
        "default": ("React + Express", "SQLite", "None")
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
    return platform_map.get(
        category,
        platform_map.get("default", ("React + Express", "SQLite", "None"))
    )

def create_structure_from_template(target_dir, platform):
    structure_text = STRUCTURE_TEMPLATES.get(platform, STRUCTURE_TEMPLATES["Web"])
    root_name = target_dir.name

    structure_text = structure_text.replace("my-web-app/", f"{root_name}/")
    structure_text = structure_text.replace("my-desktop-app/", f"{root_name}/")
    structure_text = structure_text.replace("my-hybrid-app/", f"{root_name}/")

    root, operations = parse_tree_structure(structure_text)

    for op in operations:
        if op['path'].startswith(root):
            op['path'] = op['path'].replace(root, str(target_dir), 1)

    folder_count = 0
    for op in operations:
        path = Path(op['path'])
        if op['action'] == 'CREATE_FOLDER':
            path.mkdir(parents=True, exist_ok=True)
            folder_count += 1

    print(f"  Created {folder_count} folders")
    return operations

def generate_project(options: dict, project_name: str = None, target_dir: Path = None):
    if project_name is None:
        print("\nGenerating project...\n")
        project_name = questionary.text(
            "Project name:", default="my-project"
        ).ask()

    project_name = project_name.strip().replace(" ", "-")
    target_dir = Path.cwd() / project_name

    print(f"\nCreating project: {project_name}")

    if target_dir.exists():
        print("  Removing existing directory...")
        try:
            shutil.rmtree(target_dir)
            time.sleep(0.5)
        except:
            print("  Could not remove existing directory")
            return None

    target_dir.mkdir(parents=True, exist_ok=True)

    framework, database, orm = suggest_stack(
        options["platform"],
        options["category"]
    )

    print(f"  Stack: {framework} + {database}")

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

    print("\nCreating project structure...")
    create_structure_from_template(target_dir, options["platform"])

    template_dir = Path(__file__).parent / "templates" / options["platform"].lower()

    if template_dir.exists() and any(template_dir.iterdir()):
        print("\nGenerating template files...")
        env = Environment(loader=FileSystemLoader(str(template_dir)))

        def render_directory(current_path: Path, relative_path: Path = Path(".")):
            for item in sorted(current_path.iterdir()):
                if item.is_dir():
                    render_directory(item, relative_path / item.name)
                else:
                    if item.name.endswith('.j2'):
                        output_name = item.name[:-3]
                    else:
                        output_name = item.name

                    output_path = target_dir / relative_path / output_name
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    if output_path.exists():
                        try:
                            output_path.unlink()
                            time.sleep(0.1)
                        except:
                            pass

                    if item.name.endswith('.j2'):
                        try:
                            template_path = str(
                                (relative_path / item.name).as_posix()
                            )
                            template = env.get_template(template_path)
                            content = template.render(context)
                            write_file(output_path, content)
                            print(f"  Rendered: {output_name}")
                        except Exception as e:
                            print(f"  Failed: {output_name} - {e}")
                    else:
                        try:
                            shutil.copy2(item, output_path)
                            print(f"  Copied: {output_name}")
                        except Exception as e:
                            print(f"  Failed: {output_name} - {e}")

        render_directory(template_dir)

    print("\nCreating essential files...")

    dockerfile_path = target_dir / "Dockerfile"
    if not dockerfile_path.exists():
        dockerfile_content = (
            "FROM node:18-alpine\n"
            "WORKDIR /app\n"
            "COPY package*.json ./\n"
            "RUN npm install\n"
            "COPY . .\n"
            "EXPOSE 3000\n"
            "CMD [\"npm\", \"start\"]\n"
        )
        write_file(dockerfile_path, dockerfile_content)
        print("  Created Dockerfile")

    compose_path = target_dir / "docker-compose.yml"
    if not compose_path.exists():
        compose_content = (
            "version: '3.8'\n"
            "services:\n"
            "  app:\n"
            "    build: .\n"
            "    ports:\n"
            "      - \"3000:3000\"\n"
            "    environment:\n"
            "      - DATABASE_URL=${DATABASE_URL}\n"
            "      - SECRET_KEY=${SECRET_KEY}\n"
            "    volumes:\n"
            "      - .:/app\n"
            "      - /app/node_modules\n"
        )
        write_file(compose_path, compose_content)
        print("  Created docker-compose.yml")

    env_path = target_dir / ".env.example"
    if not env_path.exists():
        env_content = (
            "# Database\n"
            "DATABASE_URL=your_database_url_here\n"
            "DB_USER=admin\n"
            "DB_PASSWORD=change_me\n"
            f"DB_NAME={project_name}\n\n"
            "# Security\n"
            "SECRET_KEY=change_this_to_random_string\n\n"
            "# App\n"
            f"APP_NAME={project_name}\n"
            "NODE_ENV=development\n"
            "PORT=3000\n"
        )
        write_file(env_path, env_content)
        print("  Created .env.example")

    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = (
            "node_modules/\n"
            "dist/\n"
            "build/\n"
            ".env\n"
            "*.log\n"
            ".DS_Store\n"
        )
        write_file(gitignore_path, gitignore_content)
        print("  Created .gitignore")

    readme_path = target_dir / "README.md"
    readme_content = (
        f"# {project_name}\n\n"
        "## Tech Stack\n"
        f"- Platform: {options['platform']}\n"
        f"- Category: {options['category']}\n"
        f"- Framework: {framework}\n"
        f"- Database: {database}\n"
        f"- ORM: {orm}\n"
        f"- Style: {options['style']}\n\n"
        "## Colors\n"
        f"{', '.join(options['colors'])}\n\n"
        "## Getting Started\n\n"
        "1. Copy environment file:\n"
        "   cp .env.example .env\n\n"
        "2. Edit .env with your secret values\n\n"
        "3. Install dependencies:\n"
        "   npm install\n\n"
        "4. Start development:\n"
        "   npm run dev\n\n"
        "## Security\n"
        "- Never commit .env files\n"
        "- Change all default passwords\n"
        "- Use strong random SECRET_KEY\n"
    )
    write_file(readme_path, readme_content)
    print("  Created README.md")

    pkg_path = target_dir / "package.json"
    if not pkg_path.exists():
        pkg_content = (
            "{\n"
            f"  \"name\": \"{project_name}\",\n"
            "  \"version\": \"1.0.0\",\n"
            "  \"description\": \"Generated project\",\n"
            "  \"main\": \"src/main.jsx\",\n"
            "  \"scripts\": {\n"
            "    \"dev\": \"vite\",\n"
            "    \"build\": \"vite build\",\n"
            "    \"start\": \"vite preview\"\n"
            "  },\n"
            "  \"dependencies\": {\n"
            "    \"react\": \"^18.2.0\",\n"
            "    \"react-dom\": \"^18.2.0\"\n"
            "  },\n"
            "  \"devDependencies\": {\n"
            "    \"@vitejs/plugin-react\": \"^4.0.0\",\n"
            "    \"vite\": \"^5.0.0\"\n"
            "  }\n"
            "}\n"
        )
        write_file(pkg_path, pkg_content)
        print("  Created package.json")

    print("\nSetting up git...")
    init_git_repo(target_dir)

    print("\n============================================================")
    print("Project ready: " + str(target_dir))
    print("============================================================")

    print("\nNext steps:")
    print("  cd " + project_name)
    print("  1. Edit .env with your secrets")
    print("  2. npm install")
    print("  3. npm run dev")

    return target_dir