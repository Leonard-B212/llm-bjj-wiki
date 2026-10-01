# Prints the available CLI commands and basic usage information.


# Prints the available CLI commands and basic usage information.


def print_help():
    print("""
LLM BJJ Wiki — Help

/write <filename> [description]           # Create a new technique note
/update <filename> [new information]      # Update an existing technique note
/check                                    # Run wiki health checks
/reindex                                  # Rebuild the vector index
/help                                     # Show this help
/exit                                     # Return to the launcher

<question>                                # Ask your BJJ wiki
                                          # Example: What attacks do I have from Side Control?

Tip: /write and /update support multiline input with /done and /cancel.
""")