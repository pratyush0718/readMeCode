from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize FastAPI app
app = FastAPI()

# Enable CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


# Load the model (BLIP used here as an example for image-to-text processing)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Process image and text prompt
def process_image_and_prompt(image: Image.Image, prompt: str) -> str:
    inputs = processor(images=image, text=prompt, return_tensors="pt")
    output = model.generate(**inputs)
    generated_text = processor.decode(output[0], skip_special_tokens=True)
    return generated_text

# Endpoint to process image and text prompt
@app.post("/process/")
async def process(image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        # Read and convert uploaded image to PIL
        image_data = await image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        # Process image and prompt
        result = process_image_and_prompt(image_pil, prompt)
        
        # Return the generated text
        return JSONResponse(content={"generated_text": result})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
