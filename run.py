"""
Simple entry point for Azure App Service.
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment (Azure sets this)
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "src.api_server.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
