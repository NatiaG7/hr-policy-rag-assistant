#!/usr/bin/env python3
"""
Optional: download HR policy documents from a URL or AWS S3 into data/raw/.

Configure via environment variables (see .env.example) or pass CLI args.
This script is a stub — replace bucket/key with your own resources.
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"


def download_from_s3(bucket: str, key: str, dest: Path) -> Path:
    try:
        import boto3
    except ImportError as e:
        raise ImportError("Install boto3: pip install boto3") from e

    dest.parent.mkdir(parents=True, exist_ok=True)
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, str(dest))
    return dest


def download_from_url(url: str, dest: Path) -> Path:
    import urllib.request

    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest


def main():
    parser = argparse.ArgumentParser(description="Download policy file to data/raw/")
    parser.add_argument("--s3-bucket", default=os.getenv("AWS_S3_BUCKET"))
    parser.add_argument("--s3-key", default=os.getenv("AWS_S3_KEY"))
    parser.add_argument("--url", default=os.getenv("POLICY_DOCUMENT_URL"))
    parser.add_argument(
        "--dest",
        type=Path,
        default=DATA_RAW / "policy.pdf",
        help="Output path under data/raw/",
    )
    args = parser.parse_args()

    if args.s3_bucket and args.s3_key:
        path = download_from_s3(args.s3_bucket, args.s3_key, args.dest)
        print(f"Downloaded from s3://{args.s3_bucket}/{args.s3_key} -> {path}")
        return

    if args.url:
        path = download_from_url(args.url, args.dest)
        print(f"Downloaded from {args.url} -> {path}")
        return

    print(
        "No source configured. Set --s3-bucket/--s3-key, --url, or env vars.\n"
        "For local demo, skip this script and use data/sample/employee_handbook_sample.txt",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
