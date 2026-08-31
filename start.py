import importlib.util
import os
import subprocess
import sys


ENV_FILE = ".env"

REQUIRED_PACKAGES = {
    "chromadb": "chromadb",
    "openai": "openai",
    "python-dotenv": "dotenv",
}


def start_wiki():
    subprocess.run([sys.executable, "-m", "app.main"])


def read_env():
    values = {}

    if not os.path.exists(ENV_FILE):
        return values

    with open(ENV_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()

    return values


def write_env(values):
    with open(ENV_FILE, "w", encoding="utf-8") as file:
        file.write(f"OPENAI_API_KEY={values.get('OPENAI_API_KEY', '')}\n")
        file.write(f"VAULT_PATH={values.get('VAULT_PATH', '')}\n")
        file.write(f"LANGUAGE={values.get('LANGUAGE', 'English')}\n")


def setup():
    print("\nFirst-time setup")
    print("----------------")

    api_key = input("OpenAI API key: ").strip()
    vault_path = input("Obsidian vault path: ").strip()
    language = input("Content language [English]: ").strip()

    if not language:
        language = "English"

    write_env({
        "OPENAI_API_KEY": api_key,
        "VAULT_PATH": vault_path,
        "LANGUAGE": language
    })

    print("\nConfiguration saved to .env")


def settings_menu():
    while True:
        values = read_env()

        print("\nSettings")
        print("--------")
        print(f"Vault path: {values.get('VAULT_PATH', 'Not configured')}")
        print(f"Content language: {values.get('LANGUAGE', 'English')}")
        print(f"OpenAI API key: {'Configured' if values.get('OPENAI_API_KEY') else 'Not configured'}")

        print("\n1. Change vault path")
        print("2. Change content language")
        print("3. Change OpenAI API key")
        print("4. Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            values["VAULT_PATH"] = input("New vault path: ").strip()
            write_env(values)
            print("\nVault path updated.")

        elif choice == "2":
            values["LANGUAGE"] = input("New content language: ").strip()
            write_env(values)
            print("\nContent language updated.")

        elif choice == "3":
            values["OPENAI_API_KEY"] = input("New OpenAI API key: ").strip()
            write_env(values)
            print("\nAPI key updated.")

        elif choice == "4":
            break

        else:
            print("\nInvalid option.")


def get_missing_packages():
    missing = []

    for package_name, import_name in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(import_name) is None:
            missing.append(package_name)

    return missing


def install_dependencies():
    print("\nInstalling dependencies...")
    print("--------------------------")

    result = subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        "requirements.txt"
    ])

    if result.returncode == 0:
        print("\nDependencies installed successfully.")
        return True

    print("\nDependency installation failed.")
    return False


def check_dependencies():
    missing = get_missing_packages()

    if not missing:
        return

    print("\nMissing dependencies:")
    for package in missing:
        print(f"- {package}")

    choice = input("\nInstall them now? (y/n): ").strip().lower()

    if choice == "y":
        install_dependencies()
    else:
        print("\nDependencies were not installed.")

def validate_configuration():
    values = read_env()

    api_key = values.get("OPENAI_API_KEY", "").strip()
    vault_path = values.get("VAULT_PATH", "").strip()

    errors = []

    if not api_key:
        errors.append("OpenAI API key is not configured.")

    if not vault_path:
        errors.append("Vault path is not configured.")
    elif not os.path.isdir(vault_path):
        errors.append(f"Vault path does not exist: {vault_path}")

    if errors:
        print("\nConfiguration error:")
        for error in errors:
            print(f"- {error}")

        print("\nOpen Settings to fix the configuration.")
        return False

    return True


def show_menu():
    while True:
        print("\n🥋 BJJ LLM Wiki")
        print("----------------")
        print("1. Start BJJ-LLM-Wiki")
        print("2. Settings")
        print("3. Install / Repair Dependencies")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            if not validate_configuration():
                continue

            missing = get_missing_packages()

            if missing:
                print("\nCannot start Wiki. Missing dependencies:")
                for package in missing:
                    print(f"- {package}")
                continue

            start_wiki()

        elif choice == "2":
            settings_menu()

        elif choice == "3":
            install_dependencies()

        elif choice == "4":
            print("\nOSS. 🤙")
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    if not os.path.exists(ENV_FILE):
        setup()

    check_dependencies()
    show_menu()