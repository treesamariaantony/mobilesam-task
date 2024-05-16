import os
import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from main import segment_everything

app = FastAPI()


@app.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    try:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        fig = segment_everything(image=image)

        output_dir = "generated"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output.png")
        fig.save(output_path)

        return FileResponse(output_path, media_type="image/png", filename="segmented_image.png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")