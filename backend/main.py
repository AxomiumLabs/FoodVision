from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from torch import nn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model
def init_model():
    model = efficientnet_b2(weights=EfficientNet_B2_Weights.DEFAULT)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=3, bias=True)
    )
    return model

# Load the model
model = init_model()
automatic_transform = EfficientNet_B2_Weights.DEFAULT.transforms()



labels = {0: "pizza", 1: "steak", 2: "sushi"}

@app.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    """Predict the food type from the uploaded image."""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if file.content_type not in allowed_types:
            return {"error": "Please upload a JPEG, PNG, or WebP image"}
            
        # Read and preprocess the image
        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as e:
            return {"error": f"Could not open image file: {str(e)}. Please upload a JPEG, PNG, or WebP image."}
            
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Apply transformations and get prediction
        try:
            raw_image = automatic_transform(image)
            
            model.eval()
            with torch.inference_mode():
                output = model(raw_image.unsqueeze(0))
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                      
            pred_prob, pred_idx = torch.max(probabilities, dim=0)
            confidence = float(pred_prob) * 100
            
            return {
                "prediction": labels[pred_idx.item()],
                "confidence": f"{confidence:.1f}%"
            }
            
        except Exception as e:
            return {"error": "Error processing image. Please try a different image."}
            
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)