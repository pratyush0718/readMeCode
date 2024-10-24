from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

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

# Load the Qwen2VL model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct", device_map="auto").to(device)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

# Function to process image and prompt using Qwen2VL model
def process_image_and_prompt(image: Image.Image, prompt: str) -> str:
    # Prepare the conversation in the required format
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt},
            ]
        }
    ]

    # Preprocess the input using the processor (image and prompt)
    text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    
    # Prepare model inputs for both the image and prompt
    inputs = processor(text=[text_prompt], images=[image], padding=True, return_tensors="pt").to(device)
    
    # Generate output from the model
    output_ids = model.generate(**inputs, max_new_tokens=512, do_sample=True)
    
    # Decode the generated IDs into text
    generated_text = processor.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    
    return generated_text[0]

# API endpoint to handle image and prompt input
@app.post("/process/")
async def process(image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        # Read and convert the uploaded image to PIL format
        image_data = await image.read()
        image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process the image and prompt using the Qwen2VL model
        result = process_image_and_prompt(image_pil, prompt)

        # Return the model's generated response
        return JSONResponse(content={"generated_text": result})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)