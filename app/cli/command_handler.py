def handle_command(user_input):
    if user_input.startswith("/"):
        parts = user_input.split(" ", 1)
        command = parts[0]

        if command == "/exit":
            return {"type": "exit"}

        if command == "/reindex":
            return {"type": "reindex"}

        if command == "/write":
            content = parts[1] if len(parts) > 1 else ""
            return {"type": "write", "content": content}
        if command == "/update":
            content = parts[1] if len(parts) > 1 else ""
            return {"type": "update", "content": content}

        return {"type": "unknown"}

    return {"type": "question", "content": user_input}