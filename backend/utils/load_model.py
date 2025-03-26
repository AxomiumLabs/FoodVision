# load the 07_effnetb2_data_20_percent_10_epochs
import torch
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights
from torch import nn
import boto3
import os
from io import BytesIO
from dotenv import load_dotenv
import socket

# Set socket timeout
socket.setdefaulttimeout(30)  # 30 seconds timeout

# Load environment variables from .env file if it exists
load_dotenv(override=True)

def validate_aws_credentials():
    """Validate that all required AWS credentials are present"""
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required AWS credentials: {', '.join(missing_vars)}")

def load_model():
    """Load the effientnetB2 model with 92 percent accuracy from S3 or local file"""   
    # S3 configuration with defaults
    bucket_name = os.getenv('S3_BUCKET_NAME')
    model_key = os.getenv('MODEL_KEY', 'models/07_effnetb2_data_20_percent_10_epochs.pt')
    
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable is required")
    
    try:
        print("Validating AWS credentials...")

        validate_aws_credentials()
        
        print("Initializing S3 client...")
        # Initialize S3 client with explicit credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        
        print(f"Checking if bucket exists: {bucket_name}")
        
        s3_client.head_bucket(Bucket=bucket_name)
        
        print(f"Downloading model from S3: {model_key}")
        response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
        model_data = response['Body'].read()
        
        print("Loading model weights...")
        # Load model weights
        weights = torch.load(BytesIO(model_data))
        
    except socket.timeout:
        raise Exception("Connection to S3 timed out. Please check your internet connection.")
    except Exception as e:
        raise Exception(f"Failed to load model from S3: {str(e)}")
    

    model = efficientnet_b2()
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=3, bias=True)
    )
    model.load_state_dict(weights)
    print("Model loaded successfully!")
    return model
    


