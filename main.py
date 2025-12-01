"""Shared Variants in COVID Diseases
This script identifies shared genetic variants between severe COVID and long COVID
based on provided CSV files containing selected features for each condition.
"""

import argparse
import re
from pathlib import Path

import pandas as pd


def parse_variants(variants_str: str) -> list[str]:
    matches = re.search(
        r"Index\(\s*\[([^\]]*)\]\s*,\s*dtype=.*\)", variants_str, flags=re.S
    )
    if not matches:
        raise ValueError("Invalid variant string format")
    inner = matches.group(1)
    variants = re.findall(r"['\"]([^'\"]+)['\"]", inner, flags=re.S)
    return variants


def main():
    parser = argparse.ArgumentParser(
        description="Variants Intersection in COVID Diseases"
    )
    parser.add_argument(
        "severe_file",
        type=Path,
        help="Path to the file containing severe COVID related variants",
    )
    parser.add_argument(
        "long_file",
        type=Path,
        help="Path to the file containing long COVID related variants",
    )
    parser.add_argument(
        "--n_variants",
        "-n",
        type=int,
        nargs="+",
        default=None,
        help="Number of variants to consider for intersection. If not provided, all "
        "available will be considered.",
    )

    args = parser.parse_args()

    severe_path: Path = args.severe_file
    long_path: Path = args.long_file
    severe_df = pd.read_csv(severe_path)
    long_df = pd.read_csv(long_path)

    if args.n_variants is None:
        n_variants_list = sorted(severe_df["n_features"].unique().tolist())
        print("No number of variants specified. Considering all available.")
    else:
        n_variants_list = args.n_variants

    for n_variants in n_variants_list:
        if n_variants not in severe_df["n_features"].values:
            raise ValueError(f"n_variants={n_variants} not found in severe COVID file.")
        if n_variants not in long_df["n_features"].values:
            raise ValueError(f"n_variants={n_variants} not found in long COVID file.")

    print("\n---- Shared Variants between Severe and Long COVID ----")

    for n_variants in n_variants_list:
        severe_line = severe_df[severe_df["n_features"] == n_variants]
        long_line = long_df[long_df["n_features"] == n_variants]

        severe_variants = parse_variants(severe_line["selected_features"].values[0])
        long_variants = parse_variants(long_line["selected_features"].values[0])

        if len(severe_variants) != n_variants:
            raise ValueError(
                f"Expected {n_variants} variants, got {len(severe_variants)}"
            )
        if len(long_variants) != n_variants:
            raise ValueError(
                f"Expected {n_variants} variants, got {len(long_variants)}"
            )

        shared_variants = set(severe_variants).intersection(set(long_variants))

        if not shared_variants:
            print(f"No shared variants for n_variants={n_variants}.")
        else:
            print(
                f"{len(shared_variants)} shared variants for n_variants={n_variants}:"
            )
            for variant in shared_variants:
                print(f"  - {variant}")


if __name__ == "__main__":
    main()
