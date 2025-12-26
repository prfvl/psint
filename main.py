import argparse
import asyncio
import sys
from utils.logger import log
from config import Config
from modules.breach import BreachChecker
from modules.metadata import MetadataExtractor 
from modules.footprint import FootprintTracker

# 1. Setup Argument Parser (CLI Interface)
parser = argparse.ArgumentParser(description="Professional OSINT Automation Tool")
subparsers = parser.add_subparsers(dest="command", help="Available modules")

# Metadata Command
meta_parser = subparsers.add_parser("metadata", help="Extract file metadata")
meta_parser.add_argument("target", help="Path to the file (image or pdf)")

# Footprint Command
footprint_parser = subparsers.add_parser("footprint", help="Trace Digital Footprint")
footprint_parser.add_argument("target", help="UPI ID to scan (e.g. name@oksbi)")

# Breach Command
breach_parser = subparsers.add_parser("breach", help="Check for email breaches")
breach_parser.add_argument("target", help="The email address to check")

async def main():
    # 2. Print Banner
    print(r"""
 ███████████   █████████  █████ ██████   █████ ███████████   
░░███░░░░░███ ███░░░░░███░░███ ░░██████ ░░███ ░█░░░███░░░█   
 ░███    ░███░███    ░░░  ░███  ░███░███ ░███ ░   ░███  ░    
 ░██████████ ░░█████████  ░███  ░███░░███░███     ░███       
 ░███░░░░░░   ░░░░░░░░███ ░███  ░███ ░░██████     ░███       
 ░███         ███    ░███ ░███  ░███  ░░█████     ░███       
 █████       ░░█████████  █████ █████  ░░█████    █████      
░░░░░         ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░    ░░░░░       
                                                                    
        -- The only OSINT tool you'll need--
    """)

    # 3. Validate Config & Parse Args
    Config.validate()
    args = parser.parse_args()

    # 4. Route Commands to Modules
    if args.command == "breach":
        module = BreachChecker()
        await module.run(args.target)
    
    elif args.command == "metadata":  
        module = MetadataExtractor()
        await module.run(args.target)

    elif args.command == "footprint":
        module = FootprintTracker()
        await module.run(args.target)

    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    
    else:
        log.error(f"Command '{args.command}' not implemented yet.")

if __name__ == "__main__":
    try:
        # Run the async loop
        asyncio.run(main())
    except KeyboardInterrupt:
        log.error("User aborted operation.")