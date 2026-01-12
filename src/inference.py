"""
Local inference script for testing without Seldon.
Provides a simple CLI for testing the model.
"""

import sys
from pathlib import Path

import joblib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def predict_sentiment(text: str, model_path: str = "models/sentiment_model.pkl") -> None:
    """
    Predict sentiment for a given text.

    Args:
        text: Text to analyze
        model_path: Path to the trained model
    """
    # Load model
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"❌ Model not found at {model_path}")
        print("Please train the model first: python src/train_model.py")
        return

    # Make prediction
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    # Display results
    emoji = "😊" if prediction == "positive" else "😞"

    print("\n" + "=" * 80)
    print(f"Text: {text}")
    print(f"\n{emoji} Sentiment: {prediction.upper()}")
    print(f"Confidence: {confidence:.1f}%")
    print(f"\nProbabilities:")
    print(f"  Negative: {probabilities[0]:.1%}")
    print(f"  Positive: {probabilities[1]:.1%}")
    print("=" * 80 + "\n")


def main() -> None:
    """Main function for CLI."""
    print("🎭 Sentiment Analyzer - Local Inference")
    print("=" * 80)

    if len(sys.argv) > 1:
        # Use text from command line argument
        text = " ".join(sys.argv[1:])
        predict_sentiment(text)
    else:
        # Interactive mode
        print("\nEnter text to analyze (or 'quit' to exit):")
        while True:
            print("\n> ", end="")
            text = input().strip()

            if text.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye! 👋")
                break

            if text:
                predict_sentiment(text)
            else:
                print("Please enter some text.")


if __name__ == "__main__":
    main()
