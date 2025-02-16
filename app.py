import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Shopify API credentials from environment variables (Set in Render)
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_ADMIN_API_KEY = os.getenv("SHOPIFY_ADMIN_API_KEY")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2023-10")

# Function to upload processed image to Shopify Files
def upload_to_shopify_files(image_url):
    files_api_url = f"{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/files.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_API_KEY
    }

    payload = {
        "file": {
            "alt": "Processed Image",
            "url": image_url
        }
    }

    response = requests.post(files_api_url, json=payload, headers=headers)
    response_data = response.json()

    # Extract and return the Shopify-hosted image URL
    if "file" in response_data:
        return response_data["file"]["url"]
    else:
        return None

# Function to update Shopify order metafield with processed image URL
def update_shopify_order_metafield(order_id, processed_image_url):
    metafield_payload = {
        "metafield": {
            "namespace": "custom",
            "key": "processed_image",
            "value": processed_image_url,
            "type": "single_line_text_field"
        }
    }

    shopify_url = f"{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}/metafields.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_API_KEY
    }

    response = requests.post(shopify_url, json=metafield_payload, headers=headers)
    return response.json()

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        image_url = data.get("image_url")
        order_id = data.get("order_id")  # Shopify order ID

        if not image_url or not order_id:
            return jsonify({"error": "Missing image_url or order_id"}), 400

        # Simulated image processing (Replace with actual processing logic)
        processed_image_url = image_url.replace("uploads", "processed")  # Dummy processing logic

        # Upload processed image to Shopify Files
        shopify_image_url = upload_to_shopify_files(processed_image_url)

        if not shopify_image_url:
            return jsonify({"error": "Failed to upload image to Shopify Files"}), 500

        # Save processed Shopify image URL to order metafield
        shopify_response = update_shopify_order_metafield(order_id, shopify_image_url)

        return jsonify({
            "original_image": image_url,
            "processed_image_url": shopify_image_url,
            "shopify_response": shopify_response,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
