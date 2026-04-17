import questionary
from project_gen.prompts import gather_project_options
from project_gen.generator import generate_project

def main():
    print("\n🚀 Project Generator – Let's build something awesome!\n")
    
    options = gather_project_options()
    
    # Show summary
    questionary.print("\n📋 Summary of your choices:", style="bold")
    for key, value in options.items():
        if key == "colors":
            print(f"  • {key}: {', '.join(value)}")
        else:
            print(f"  • {key}: {value}")
    
    if not questionary.confirm("\nProceed with generation?").ask():
        print("❌ Aborted.")
        return
    
    generate_project(options)
    print("\n✅ Project generated successfully!")

if __name__ == "__main__":
    main()