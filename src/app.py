"""
FastAPI application for sentiment analysis UI.
This app provides a web interface and calls the Seldon inference server.
"""

import logging
import os
from typing import Dict

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
    description="Sentiment analysis using Seldon Core",
    version=os.getenv("APP_VERSION", "0.1.0"),
)

# Set up templates
templates = Jinja2Templates(directory="src/templates")

# Model server configuration
MODEL_SERVER_HOST = os.getenv("MODEL_SERVER_HOST", "localhost")
MODEL_SERVER_PORT = os.getenv("MODEL_SERVER_PORT", "8001")

# Construct model server URL
MODEL_SERVER_URL = f"http://{MODEL_SERVER_HOST}:{MODEL_SERVER_PORT}/predict"


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
        # Call model server
        logger.info(f"Analyzing text: {text[:50]}...")
        prediction = await call_model_server(text)

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


async def call_model_server(text: str) -> Dict[str, str]:
    """
    Call the model server API.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with prediction results

    Raises:
        HTTPException: If the API call fails
    """
    # Prepare request payload
    payload = {"text": text}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(MODEL_SERVER_URL, json=payload)
            response.raise_for_status()

            # Parse response
            result = response.json()
            logger.debug(f"Model server response: {result}")

            # Extract prediction
            prediction = result.get("prediction")
            probability = result.get("probability", 0.0)

            return {"sentiment": prediction, "text": text, "confidence": probability}

    except httpx.HTTPStatusError as e:
        logger.error(f"Model server returned error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to model server: {e}")
        raise HTTPException(status_code=503, detail=f"Cannot connect to model server: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check() -> Dict[str, str]:
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
