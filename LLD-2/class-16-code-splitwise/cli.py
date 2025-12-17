#!/usr/bin/env python
"""
Splitwise CLI Application
Main entry point for command-line interface using Command Design Pattern.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'splitwise_project.settings')
django.setup()

from splitwise_app.commands import CommandInvoker, CommandParser


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗██████╗ ██╗     ██╗████████╗██╗    ██╗██╗███████╗███████╗         ║
║   ██╔════╝██╔══██╗██║     ██║╚══██╔══╝██║    ██║██║██╔════╝██╔════╝         ║
║   ███████╗██████╔╝██║     ██║   ██║   ██║ █╗ ██║██║███████╗█████╗           ║
║   ╚════██║██╔═══╝ ██║     ██║   ██║   ██║███╗██║██║╚════██║██╔══╝           ║
║   ███████║██║     ███████╗██║   ██║   ╚███╔███╔╝██║███████║███████╗         ║
║   ╚══════╝╚═╝     ╚══════╝╚═╝   ╚═╝    ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝         ║
║                                                                               ║
║                       Command-Line Expense Manager                           ║
║                         Type 'HELP' for commands                             ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main CLI loop."""
    print_banner()

    invoker = CommandInvoker()
    parser = CommandParser()

    print("\nWelcome to Splitwise CLI!")
    print("Type 'HELP' to see available commands or 'EXIT' to quit.\n")

    while True:
        try:
            # Get user input
            user_input = input("splitwise> ").strip()

            if not user_input:
                continue

            # Check for exit
            if user_input.upper() == 'EXIT':
                print("\nThank you for using Splitwise! Goodbye! 👋")
                break

            # Check for help
            if user_input.upper() == 'HELP':
                print(parser.show_help())
                continue

            # Parse and execute command
            command = parser.parse(user_input)

            if command:
                result = invoker.execute_command(command)
                print(result)

        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye! 👋")
            break

        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == '__main__':
    main()
