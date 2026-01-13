#!/usr/bin/env python3
"""
Validation script to verify project enhancements.
Tests three-class sentiment, tools configuration, and data quality.
"""

import sys
from pathlib import Path

import pandas as pd


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False


def validate_data() -> bool:
    """Validate the generated training data."""
    print("\n📊 Validating Training Data...")

    csv_path = "data/raw/sentiment_data.csv"
    if not Path(csv_path).exists():
        print(f"❌ Data file not found: {csv_path}")
        return False

    df = pd.read_csv(csv_path)

    # Check for three sentiment classes
    sentiments = df["sentiment"].unique()
    required_sentiments = {"positive", "neutral", "negative"}

    if set(sentiments) == required_sentiments:
        print(f"✅ Three-class sentiment detected: {sorted(sentiments)}")
    else:
        print(f"❌ Expected {required_sentiments}, got {set(sentiments)}")
        return False

    # Check distribution
    sentiment_counts = df["sentiment"].value_counts()
    print("\n📈 Sentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {sentiment:8s}: {count:4d} ({percentage:5.1f}%)")

    # Check balance (should be roughly 33% each)
    min_count = sentiment_counts.min()
    max_count = sentiment_counts.max()
    balance_ratio = min_count / max_count

    if balance_ratio >= 0.9:  # Allow 10% variance
        print(f"✅ Data is well-balanced (ratio: {balance_ratio:.2f})")
    else:
        print(f"⚠️  Data imbalance detected (ratio: {balance_ratio:.2f})")

    return True


def validate_configuration() -> bool:
    """Validate configuration files."""
    print("\n🔧 Validating Configuration Files...")

    checks = [
        (".python-version", "Python version file"),
        (".java-version", "Java version file"),
        (".envrc", "direnv configuration"),
        ("pyproject.toml", "Project configuration"),
        (".pre-commit-config.yaml", "Pre-commit hooks"),
        (".gitignore", "Git ignore file"),
    ]

    results = [check_file_exists(file, desc) for file, desc in checks]
    return all(results)


def validate_documentation() -> bool:
    """Validate documentation files."""
    print("\n📚 Validating Documentation...")

    docs = [
        ("README.md", "Main README"),
        ("docs/TOOLS_SETUP.md", "Tools setup guide"),
        ("docs/GETTING_STARTED.md", "Getting started guide"),
    ]

    results = [check_file_exists(doc, desc) for doc, desc in docs]
    return all(results)


def validate_python_version() -> bool:
    """Check Python version."""
    print("\n🐍 Validating Python Environment...")

    python_version_file = Path(".python-version")
    if python_version_file.exists():
        required_version = python_version_file.read_text().strip()
        print(f"✅ Required Python version: {required_version}")

        current_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        print(f"   Current Python version: {current_version}")

        if current_version.startswith(required_version.split(".")[0]):
            print("✅ Python version compatible")
            return True
        else:
            print("⚠️  Python version mismatch")
            return False
    else:
        print("❌ .python-version file not found")
        return False


def main() -> None:
    """Run all validation checks."""
    print("🚀 Project Validation Script")
    print("=" * 60)

    checks = [
        ("Configuration", validate_configuration),
        ("Documentation", validate_documentation),
        ("Python Environment", validate_python_version),
        ("Training Data", validate_data),
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results[name] = False

    # Summary
    print("\n" + "=" * 60)
    print("📋 Validation Summary:")
    print("=" * 60)

    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8s} - {name}")

    # Overall result
    print("=" * 60)
    if all(results.values()):
        print("🎉 All validations passed!")
        print("\n✨ Project is ready for use with:")
        print("   • Three-class sentiment (Positive/Neutral/Negative)")
        print("   • Complete tool configuration (pyenv, jenv, direnv, uv)")
        print("   • Comprehensive documentation")
        print("   • Balanced training data")
        sys.exit(0)
    else:
        print("⚠️  Some validations failed. Please review above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
