import argparse
from file_checker import extract, compare, report

def main():
    parser = argparse.ArgumentParser(
        description="FileChecker - Android File Integrity CLI Tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # === Extract Command ===
    extract_parser = subparsers.add_parser("extract", help="Extract files and generate snapshot")
    extract_parser.add_argument("--device", required=True, help="Device number (e.g., 001)")
    extract_parser.add_argument("--dir", default="/sdcard/DCIM", help="Remote path to pull")

    # === Compare Command ===
    compare_parser = subparsers.add_parser("compare", help="Compare baseline and new snapshots")
    compare_parser.add_argument("--device", required=True, help="Device number (e.g., 001)")

    # === Report Command ===
    report_parser = subparsers.add_parser("report", help="Generate forensic report from comparison")
    report_parser.add_argument("--device", required=True, help="Device number (e.g., 001)")
    report_parser.add_argument("--format", nargs="+", default=["csv", "txt"],
                               help="Report formats to generate (e.g., csv txt)")

    # === Dispatch Commands ===
    args = parser.parse_args()

    if args.command == "extract":
        print("[DEBUG] extract command triggered")
        extract.run(args.device, args.dir)

    elif args.command == "compare":
        print("[DEBUG] compare command triggered")
        compare.run(args.device)

    elif args.command == "report":
        print("[DEBUG] report command triggered")
        report.run(args.device, args.format)
