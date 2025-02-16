import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Shopify API Credentials (use environment variables)
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def upload_to_shopify_files(image_url):
    """Uploads the processed image to Shopify Files API and returns the Shopify-hosted URL."""
    shopify_url = f"{SHOPIFY_STORE_URL}/admin/api/2024-01/files.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }
    data = {
        "file": {
            "url": image_url
        }
    }
    
    response = requests.post(shopify_url, json=data, headers=headers)
    response_data = response.json()
    
    if "file" in response_data:
        return response_data["file"]["url"]
    else:
        print("Shopify File Upload Error:", response_data)
        return None

def update_order_metafield(order_id, shopify_file_url):
    """Updates the Shopify order metafield with the Shopify-hosted file URL."""
    shopify_url = f"{SHOPIFY_STORE_URL}/admin/api/2024-01/metafields.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }
    data = {
        "metafield": {
            "namespace": "custom",
            "key": "processed_image",
            "value": shopify_file_url,
            "type": "url",
            "owner_id": order_id,
            "owner_resource": "order"
        }
    }
    
    response = requests.post(shopify_url, json=data, headers=headers)
    return response.json()

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    image_url = data.get("image_url")
    order_id = data.get("order_id")

    if not image_url or not order_id:
        return jsonify({"error": "Missing image_url or order_id"}), 400

    # Step 1: Upload processed image to Shopify
    shopify_file_url = upload_to_shopify_files(image_url)
    
    if not shopify_file_url:
        return jsonify({"error": "Failed to upload image to Shopify"}), 500

    # Step 2: Update metafield with Shopify-hosted image URL
    metafield_response = update_order_metafield(order_id, shopify_file_url)

    return jsonify({
        "original_image": image_url,
        "processed_image_url": shopify_file_url,
        "shopify_response": metafield_response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
