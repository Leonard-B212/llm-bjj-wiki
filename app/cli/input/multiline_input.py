# Provides safe multiline terminal input for longer CLI content.
# Keeps long descriptions separate from command history and single-line commands.


def read_multiline(
    prompt="Enter description:",
    end_marker="/done",
    cancel_marker="/cancel",
):
    print(f"\n{prompt}")
    print(
        f"Enter {end_marker} to finish or "
        f"{cancel_marker} to cancel.\n"
    )

    lines = []

    while True:
        line = input("> ")
        command = line.strip().lower()

        if command == end_marker:
            return "\n".join(lines).strip()

        if command == cancel_marker:
            return None

        lines.append(line)