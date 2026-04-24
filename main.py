#!/usr/bin/env python3
"""
main.py – Unified entry point.

Usage:
  python main.py          → interactive CLI
  python main.py --web    → start web server (UI + API)
  python main.py --web --port 8080
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Project Generator – scaffold a full-stack app instantly"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start the web UI + REST API server instead of interactive CLI",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5050,
        help="Port for the web server (default: 5050)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for the web server (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for the web server",
    )

    args = parser.parse_args()

    if args.web:
        from project_gen.server import run_server
        run_server(host=args.host, port=args.port, debug=args.debug)
    else:
        from project_gen.cli import main as cli_main
        cli_main()


if __name__ == "__main__":
    main()
