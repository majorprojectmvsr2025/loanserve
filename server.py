import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="ZIP Server for Code Sync")

@app.get("/")
def root():
    return {"message": "Server is running. Use /download/{week_number} to download a ZIP."}

@app.get("/download/{week_number}")
def download_zip(week_number: int):
    # Ensure week number is between 1 and 8
    if week_number < 1 or week_number > 8:
        raise HTTPException(status_code=400, detail="Invalid week number. Must be between 1 and 8.")
        
    filename = f"Week_{week_number}_Cumulative.zip"
    filepath = os.path.join(os.path.dirname(__file__), "zips", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"File {filename} not found on server.")
        
    return FileResponse(filepath, media_type="application/zip", filename=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
