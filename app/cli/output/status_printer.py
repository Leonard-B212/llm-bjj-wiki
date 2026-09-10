GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def format_success(message):
    return f"{GREEN}[OK]{RESET} {message}"


def format_warning(message):
    return f"{YELLOW}[WARN]{RESET} {message}"


def print_success(message):
    print(format_success(message))


def print_warning(message):
    print(format_warning(message))