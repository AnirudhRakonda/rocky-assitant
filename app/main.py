"""
Rocky Assistant main entry point.

Run this script to start the alien communication system.
"""

import sys
import argparse
import os

# Ensure app module is importable (add parent directory to path)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from app.utils import logger
from app.pipeline import get_assistant


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Rocky Assistant - Alien Communication System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start interactive mode
  python main.py

  # Test with specific input
  python main.py --test "Hello Rocky"
  
  # List audio devices
  python main.py --list-devices
  
  # Run from project root - not from app/ directory!
  cd /Users/anirudhrakonda/Desktop/rocky/rocky-assistant
  source venv/bin/activate
  python app/main.py
        """
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Test mode: provide a single input string"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List available audio devices and exit"
    )

    args = parser.parse_args()

    try:
        # Handle device listing
        if args.list_devices:
            print("\n" + "="*60)
            print("Available Audio Devices")
            print("="*60 + "\n")
            try:
                import sounddevice as sd
                print(sd.query_devices())
                print("\n" + "="*60)
                print("To specify a device, update SOUNDDEVICE config")
                print("="*60 + "\n")
            except Exception as e:
                print(f"Error querying devices: {e}")
            sys.exit(0)

        # Set debug mode if requested
        if args.debug:
            os.environ["DEBUG_MODE"] = "true"
            os.environ["LOG_LEVEL"] = "DEBUG"

        logger.info("="*60)
        logger.info("🎵 ROCKY ASSISTANT STARTING 🎵")
        logger.info("="*60)

        # Initialize assistant
        assistant = get_assistant()

        # Run
        assistant.run(test_input=args.test)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
