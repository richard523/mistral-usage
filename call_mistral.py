# call_mistral.py
from mistralai.client import Mistral
from mistral_usage_tracker import log_token_usage
from dotenv import load_dotenv
import os
import time
import threading
import argparse
import json

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Call Mistral API with a prompt.")
parser.add_argument("prompt", type=str, help="The prompt to send to Mistral API.")
args = parser.parse_args()

# Load API key from .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file.")

# Variable to control the counter thread
counter_active = True

# Function to display the counter
def display_counter():
    counter = 0
    while counter_active:
        print(f"Waiting for response... {counter} seconds", end="\r")
        time.sleep(1)
        counter += 1

# Start the counter thread
counter_thread = threading.Thread(target=display_counter)
counter_thread.start()

# Start timing
start_time = time.time()

# Initialize Mistral client
with Mistral(api_key=api_key) as client:
    # Example API call
    response = client.chat.complete(
        model="mistral-medium-latest",
        messages=[{"role": "user", "content": args.prompt}]
    )

    # Stop the counter thread
    counter_active = False
    counter_thread.join()

    # Log token usage
    log_token_usage(response, "mistral-medium-latest")
    
    # End timing
    end_time = time.time()
    
    # Calculate and log the duration
    duration = end_time - start_time
    print(f"\nRequest took {duration:.2f} seconds to complete.")
    
    # Print the received message
    print("\nReceived message:")
    print(response.choices[0].message.content)
    
    # Print all metadata
    print("\nFull response metadata:")
    print(json.dumps(response.model_dump(), indent=2))
    
    print("\nToken usage logged!")
