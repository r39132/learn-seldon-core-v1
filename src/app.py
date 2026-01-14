"""
FastAPI application for sentiment analysis UI.
This app provides a web interface and calls the Seldon Core v1 inference API.
"""

import logging
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analyzer",
    description="Sentiment analysis using Seldon Core v1",
    version=os.getenv("APP_VERSION", "0.1.0"),
)

# Set up templates
templates = Jinja2Templates(directory="src/templates")

# Seldon Core configuration
SELDON_HOST = os.getenv("SELDON_HOST", "localhost")
SELDON_PORT = os.getenv("SELDON_PORT", "8080")
SELDON_DEPLOYMENT_NAME = os.getenv("SELDON_DEPLOYMENT_NAME", "sentiment-classifier")
SELDON_NAMESPACE = os.getenv("SELDON_NAMESPACE", "seldon")

# Construct Seldon API URL (Seldon Core v1 format)
SELDON_API_URL = f"http://{SELDON_HOST}:{SELDON_PORT}/api/v1.0/predictions"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """
    Render the home page with the sentiment analysis form.

    Args:
        request: FastAPI request object

    Returns:
        HTML response
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_sentiment(request: Request, text: str = Form("")) -> HTMLResponse:
    """
    Analyze sentiment of the provided text.

    Args:
        request: FastAPI request object
        text: Text to analyze

    Returns:
        HTML response with analysis result
    """
    if not text or not text.strip():
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": None, "error": "Please enter some text to analyze."},
        )

    try:
        # Call Seldon Core API
        logger.info(f"Analyzing text: {text[:50]}...")
        prediction = await call_seldon_api(text)

        logger.info(f"Prediction: {prediction}")

        return templates.TemplateResponse(
            "index.html", {"request": request, "result": prediction, "input_text": text}
        )

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": f"Error analyzing sentiment: {str(e)}",
                "input_text": text,
            },
        )


async def call_seldon_api(text: str) -> dict[str, Any]:
    """
    Call the Seldon Core v1 API.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with prediction results

    Raises:
        HTTPException: If the API call fails
    """
    # Prepare Seldon Core v1 request payload
    # Format: {"data": {"ndarray": [["text"]]}}
    payload = {"data": {"ndarray": [[text]]}}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(SELDON_API_URL, json=payload)
            response.raise_for_status()

            # Parse Seldon response
            result = response.json()
            logger.debug(f"Seldon API response: {result}")

            # Extract prediction from Seldon Core v1 format
            # Response: {"data": {"ndarray": [["positive", 0.95]]}}
            # or {"names": [...], "ndarray": [[...]]}
            data = result.get("data", {})
            ndarray = data.get("ndarray", [])

            if ndarray and len(ndarray) > 0:
                prediction_data = ndarray[0]
                if isinstance(prediction_data, list) and len(prediction_data) >= 2:
                    sentiment = prediction_data[0]
                    confidence = float(prediction_data[1])
                else:
                    sentiment = str(prediction_data[0]) if prediction_data else "unknown"
                    confidence = 0.0
            else:
                sentiment = "unknown"
                confidence = 0.0

            return {"sentiment": sentiment, "text": text, "confidence": confidence}

    except httpx.HTTPStatusError as e:
        logger.error(f"Seldon API returned error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e)) from e
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Seldon API: {e}")
        raise HTTPException(
            status_code=503, detail=f"Cannot connect to Seldon API at {SELDON_API_URL}: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy", "service": "sentiment-analyzer-ui"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("FASTAPI_PORT", "8000"))
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")

    uvicorn.run(app, host=host, port=port)
