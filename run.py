"""
Simple entry point for Azure App Service.
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment (Azure uses WEBSITES_PORT)
    port = int(os.environ.get("WEBSITES_PORT", 8000))

    uvicorn.run(
        "src.api_server.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
