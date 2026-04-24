import questionary
from project_gen.prompts import gather_project_options
from project_gen.generator import generate_project

def main():
    print("\n🚀 Project Generator - Let's build something awesome!\n")
    options = gather_project_options()

    print("\n" + "="*60)
    print("📋 Summary:")
    print(f"  Platform: {options['platform']}")
    print(f"  Category: {options['category']}")
    print(f"  Colors: {', '.join(options['colors'])}")
    print(f"  Style: {options['style']}")
    print(f"  Scope: {options['scope']}")
    print("="*60)

    if not questionary.confirm("\nProceed with generation?").ask():
        print("❌ Aborted.")
        return

    generate_project(options)
    print("\n✅ Project generated successfully!")

if __name__ == "__main__":
    main()