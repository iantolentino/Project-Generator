"""
cli.py – Interactive terminal entry point for project-gen.
"""

import sys
import questionary
from colorama import init as colorama_init, Fore, Style

from project_gen.prompts import gather_project_options
from project_gen.generator import generate_project_to_disk
from project_gen.stacks import STACK_META, resolve_stack

colorama_init(autoreset=True)


BANNER = f"""{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════╗
║          🚀  Project Generator  v2.0                 ║
║   Full-stack scaffolding in seconds – just edit      ║
║   your .env and you're ready to build.               ║
╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""


def main():
    print(BANNER)

    try:
        options = gather_project_options()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Aborted.{Style.RESET_ALL}")
        sys.exit(0)

    project_name = options.pop("project_name")
    stack_id = resolve_stack(options["platform"], options["category"])
    meta = STACK_META.get(stack_id, {})

    # ── Summary ───────────────────────────────────────
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📋  Project Summary{Style.RESET_ALL}")
    print(f"  {'Name':<12} {Fore.WHITE}{project_name}{Style.RESET_ALL}")
    print(f"  {'Platform':<12} {Fore.WHITE}{options['platform']}{Style.RESET_ALL}")
    print(f"  {'Category':<12} {Fore.WHITE}{options['category']}{Style.RESET_ALL}")
    print(f"  {'Stack':<12} {Fore.GREEN}{meta.get('label', stack_id)}{Style.RESET_ALL}")
    print(f"  {'Style':<12} {Fore.WHITE}{options['style']}{Style.RESET_ALL}")
    print(f"  {'Scope':<12} {Fore.WHITE}{options['scope']}{Style.RESET_ALL}")
    if meta.get("tags"):
        print(f"  {'Tags':<12} {Fore.CYAN}{', '.join(meta['tags'])}{Style.RESET_ALL}")

    if not questionary.confirm("\n  Proceed with generation?", default=True).ask():
        print(f"{Fore.YELLOW}Cancelled.{Style.RESET_ALL}")
        sys.exit(0)

    # ── Generate ──────────────────────────────────────
    print(f"\n{Fore.CYAN}⏳  Generating project files...{Style.RESET_ALL}")
    try:
        target_dir, stack_id, meta = generate_project_to_disk(options, project_name)
    except Exception as e:
        print(f"{Fore.RED}❌  Generation failed: {e}{Style.RESET_ALL}")
        sys.exit(1)

    # ── Success ───────────────────────────────────────
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅  Project ready!{Style.RESET_ALL}")
    print(f"   📁  {target_dir}\n")

    print(f"{Fore.CYAN}{Style.BRIGHT}🔑  Next steps:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}1. cd {project_name}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}2. cp .env.example .env{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}3. Fill in secret values in .env  ← only thing you need to edit!{Style.RESET_ALL}")

    # Stack-specific quick-start
    if stack_id == "nextjs_postgres_prisma":
        print(f"   {Fore.WHITE}4. npm install && npm run db:push && npm run db:seed && npm run dev{Style.RESET_ALL}")
    elif stack_id == "react_node_mongo":
        print(f"   {Fore.WHITE}4. cd server && npm install && npm run seed && npm run dev{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}5. cd ../client && npm install && npm run dev{Style.RESET_ALL}")
    elif stack_id == "django_postgres":
        print(f"   {Fore.WHITE}4. python -m venv venv && source venv/bin/activate{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}5. pip install -r requirements.txt{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}6. python manage.py migrate && python manage.py createsuperuser && python manage.py runserver{Style.RESET_ALL}")
    elif stack_id == "vue_express_mysql":
        print(f"   {Fore.WHITE}4. cd server && npm install && node src/sync-db.js && npm run dev{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}5. cd ../client && npm install && npm run dev{Style.RESET_ALL}")
    elif stack_id == "react_static":
        print(f"   {Fore.WHITE}4. npm install && npm run dev{Style.RESET_ALL}")
    elif stack_id in ("electron_sqlite", "tauri_react"):
        print(f"   {Fore.WHITE}4. npm install && npm run dev{Style.RESET_ALL}")

    print(f"\n   {Fore.CYAN}Or use Docker: docker-compose up -d{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Happy coding! 🎉{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
