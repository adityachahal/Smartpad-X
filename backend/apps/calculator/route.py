from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    try:
        image_data = base64.b64decode(data.image.split(",")[1])
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)

        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        print("Analyze image function output:", responses)

        if not responses:
            return {"message": "No valid response from analyze_image", "data": [], "status": "failure"}
        
        data = []
        for response in responses:
            data.append(response)
            print('Response:', response)

        return {"message": "Image processed", "data": data, "status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred", "error": str(e), "status": "failure"}
