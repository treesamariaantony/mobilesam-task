import os
import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from main import segment_everything

app = FastAPI()

@app.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    fig = segment_everything(image=image)

    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.png")
    fig.save(output_path)

    return FileResponse(output_path, media_type="image/png", filename="segmented_image.png")
