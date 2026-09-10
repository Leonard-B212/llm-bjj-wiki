GREEN = "\033[32m"
RESET = "\033[0m"


def format_success(message):
    return f"{GREEN}[OK]{RESET} {message}"


def print_success(message):
    print(format_success(message))