# load the 07_effnetb2_data_20_percent_10_epochs
import torch
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from torch import nn
import boto3
from botocore.config import Config
import os
from io import BytesIO
from dotenv import load_dotenv
import time



load_dotenv(override=True)


def load_model():
    """Load the effientnetB2 model with 92 percent accuracy from S3 or local file"""   
    # Check if we should load from S3
    use_s3 = os.getenv('USE_S3', 'false').lower() == 'true'
    
    if use_s3:
        # S3 configuration
        bucket_name = os.getenv('S3_BUCKET_NAME')
        model_key = os.getenv('MODEL_KEY', 'models/07_effnetb2_data_20_percent_10_epochs.pt')
        
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required when USE_S3 is true")
            
        # Initialize S3 client with timeouts
        s3_config = Config(
            connect_timeout=10,
            read_timeout=30,
            retries={'max_attempts': 2}
        )
        s3_client = boto3.client('s3', config=s3_config)
        
        # Download model from S3
        try:
            print("Starting S3 download...")
            start_time = time.time()
            
            response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
            print(f"Got S3 response in {time.time() - start_time:.2f} seconds")
            
            # Read data in chunks with progress
            data = []
            total_size = response['ContentLength']
            bytes_read = 0
            
            print("Reading model data...")
            for chunk in response['Body'].iter_chunks(chunk_size=8192):
                data.append(chunk)
                bytes_read += len(chunk)
                progress = (bytes_read / total_size) * 100
                print(f"Download progress: {progress:.1f}% ({bytes_read}/{total_size} bytes)")
            
            print(f"Finished reading data in {time.time() - start_time:.2f} seconds")
            model_data = b''.join(data)
            
            print("Loading model weights...")
            weights = torch.load(BytesIO(model_data))
            print("Model loaded from S3")
            
        except Exception as e:
            print(f"Failed to load model from S3: {str(e)}")
            print("Falling back to local file...")
            weights = torch.load("models/07_effnetb2_data_20_percent_10_epochs.pt")
    else:
        # Load from local file
        print("Loading model from local file")
        weights = torch.load("models/07_effnetb2_data_20_percent_10_epochs.pt")
    
    # Create and configure model
    model = efficientnet_b2()
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=3, bias=True)
    )
    model.load_state_dict(weights)
    return model
    


