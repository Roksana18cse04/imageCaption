from fastapi import APIRouter, UploadFile, File, Form
from app.services.image_service import generate_caption_from_image_and_instruction
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/generate-caption")
async def generate_caption(
    file: UploadFile = File(...),
    instruction: str = Form(...)
):
    try:
        # Save uploaded image temporarily
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Generate caption
        caption = generate_caption_from_image_and_instruction(file_location, instruction)

        # Delete temp file
        import os
        os.remove(file_location)

        return JSONResponse(content={"caption": caption}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
