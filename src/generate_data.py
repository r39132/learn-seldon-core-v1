"""
Data generation script for sentiment analysis.
Generates labeled training data with positive and negative sentiment examples.
"""

import json
import os
import random
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SentimentDataGenerator:
    """Generate labeled sentiment data for training."""

    def __init__(self, num_samples: int = 1000, seed: int = 42) -> None:
        """
        Initialize the data generator.

        Args:
            num_samples: Number of samples to generate
            seed: Random seed for reproducibility
        """
        self.num_samples = num_samples
        random.seed(seed)

        # Sample positive and negative phrases
        self.positive_templates = [
            "I absolutely love {product}! It's amazing!",
            "This {product} exceeded my expectations. Highly recommend!",
            "Best {product} I've ever used. Five stars!",
            "So happy with my {product} purchase. Excellent quality!",
            "The {product} is fantastic! Worth every penny.",
            "I'm thrilled with this {product}. Outstanding!",
            "Couldn't be happier with my {product}. Perfect!",
            "This {product} is brilliant. Totally satisfied!",
            "Wonderful {product}! Will definitely buy again.",
            "Amazing {product}! Exceeded all my hopes.",
            "The {product} is incredible. Best decision ever!",
            "Really impressed with this {product}. Great value!",
            "Absolutely satisfied with the {product}. Superb quality!",
            "Love everything about this {product}!",
            "This {product} is awesome! Can't stop using it.",
            "This {product} is rad! Totally worth it!",
            "The {product} is rad. Best purchase ever!",
            "So rad! This {product} rocks!",
        ]

        self.negative_templates = [
            "Terrible {product}. Complete waste of money.",
            "Very disappointed with this {product}. Poor quality.",
            "The {product} broke after one day. Horrible!",
            "Would not recommend this {product} to anyone. Awful!",
            "Worst {product} ever. Total disappointment.",
            "This {product} is garbage. Save your money.",
            "Extremely unhappy with the {product}. Defective!",
            "The {product} is terrible. Regret buying it.",
            "Don't buy this {product}. It's useless!",
            "Awful {product}. Nothing works as advertised.",
            "Horrible experience with this {product}. Very poor!",
            "The {product} is a complete letdown. Disappointing!",
            "This {product} is junk. Waste of time and money.",
            "Really bad {product}. Doesn't work at all.",
            "Terrible quality {product}. Would return if I could.",
            "This {product} is meh. Not worth the money.",
            "The {product} is pretty meh. Very disappointing.",
            "Meh, this {product} doesn't work well.",
        ]

        self.neutral_templates = [
            "The {product} is okay. Nothing special.",
            "This {product} works as expected. Average.",
            "The {product} is fine for the price.",
            "Got this {product} yesterday. It's alright.",
            "The {product} does what it's supposed to do.",
            "This {product} is decent. Not great, not terrible.",
            "The {product} is acceptable. Could be better.",
            "It's a standard {product}. Nothing remarkable.",
            "The {product} meets basic expectations.",
            "This {product} is neither good nor bad.",
            "The {product} works fine. No complaints.",
            "Average {product}. Gets the job done.",
            "The {product} is adequate for my needs.",
            "This {product} is pretty standard. No surprises.",
            "The {product} is mediocre. Just okay.",
        ]

        self.products = [
            "smartphone",
            "laptop",
            "headphones",
            "coffee maker",
            "vacuum cleaner",
            "camera",
            "tablet",
            "watch",
            "speaker",
            "monitor",
            "keyboard",
            "mouse",
            "charger",
            "case",
            "stand",
            "adapter",
            "cable",
            "battery",
            "backpack",
            "desk",
        ]

    def generate_samples(self) -> list[tuple[str, str]]:
        """
        Generate samples with labels.

        Returns:
            List of tuples (text, label)
        """
        samples = []

        # Generate roughly equal positive, neutral, and negative samples
        num_positive = self.num_samples // 3
        num_neutral = self.num_samples // 3
        num_negative = self.num_samples - num_positive - num_neutral

        # Generate positive samples
        for _ in range(num_positive):
            template = random.choice(self.positive_templates)
            product = random.choice(self.products)
            text = template.format(product=product)
            samples.append((text, "positive"))

        # Generate neutral samples
        for _ in range(num_neutral):
            template = random.choice(self.neutral_templates)
            product = random.choice(self.products)
            text = template.format(product=product)
            samples.append((text, "neutral"))

        # Generate negative samples
        for _ in range(num_negative):
            template = random.choice(self.negative_templates)
            product = random.choice(self.products)
            text = template.format(product=product)
            samples.append((text, "negative"))

        # Shuffle samples
        random.shuffle(samples)

        return samples

    def save_to_csv(self, output_path: str) -> None:
        """
        Generate and save samples to CSV file.

        Args:
            output_path: Path to save the CSV file
        """
        samples = self.generate_samples()
        df = pd.DataFrame(samples, columns=["text", "sentiment"])

        # Create directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"Generated {len(samples)} samples and saved to {output_path}")
        print(f"Positive samples: {len(df[df['sentiment'] == 'positive'])}")
        print(f"Neutral samples: {len(df[df['sentiment'] == 'neutral'])}")
        print(f"Negative samples: {len(df[df['sentiment'] == 'negative'])}")

    def save_to_json(self, output_path: str) -> None:
        """
        Generate and save samples to JSON file.

        Args:
            output_path: Path to save the JSON file
        """
        samples = self.generate_samples()
        data = [{"text": text, "sentiment": label} for text, label in samples]

        # Create directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save to JSON
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Generated {len(samples)} samples and saved to {output_path}")


def main() -> None:
    """Main function to generate training data."""
    # Get configuration from environment
    raw_data_path = os.getenv("RAW_DATA_PATH", "data/raw")
    num_samples = 1000
    seed = int(os.getenv("RANDOM_SEED", "42"))

    # Initialize generator
    generator = SentimentDataGenerator(num_samples=num_samples, seed=seed)

    # Generate and save data
    csv_path = f"{raw_data_path}/sentiment_data.csv"
    json_path = f"{raw_data_path}/sentiment_data.json"

    generator.save_to_csv(csv_path)
    generator.save_to_json(json_path)


if __name__ == "__main__":
    main()
