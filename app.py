import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Shopify Credentials from Environment Variables
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")  # Example: "your-store.myshopify.com"
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")  # Private App API Key

# Shopify API Endpoints
SHOPIFY_FILES_API_URL = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-01/files.json"
SHOPIFY_METAFIELD_API_URL = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-01/orders/{{order_id}}/metafields.json"

def upload_image_to_shopify(image_url):
    """
    Uploads an image from DigitalOcean Spaces to Shopify Files API
    Returns the Shopify-hosted image URL or None if upload fails.
    """
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "file": {
            "alt": "Processed Pet Portrait",
            "url": image_url  # DigitalOcean Processed Image URL
        }
    }

    response = requests.post(SHOPIFY_FILES_API_URL, json=payload, headers=headers)
    response_data = response.json()

    if "file" in response_data:
        return response_data["file"]["url"]  # Shopify-hosted URL
    else:
        return None  # Return None if upload fails

def update_shopify_order_metafield(order_id, shopify_image_url):
    """
    Updates the order metafield in Shopify with the Shopify-hosted image URL.
    """
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    metafield_data = {
        "metafield": {
            "namespace": "custom",
            "key": "processed_image",
            "value": shopify_image_url,
            "type": "single_line_text_field"
        }
    }

    response = requests.post(SHOPIFY_METAFIELD_API_URL.format(order_id=order_id), json=metafield_data, headers=headers)
    return response.json()

@app.route('/process', methods=['POST'])
def process_image():
    """
    Handles the image processing request.
    Receives an image URL & order ID, processes the image, 
    uploads it to Shopify, and updates the order metafield.
    """
    data = request.get_json()
    image_url = data.get("image_url")
    order_id = data.get("order_id")

    if not image_url or not order_id:
        return jsonify({"error": "Missing image_url or order_id"}), 400

    try:
        # Step 1: Process the image (assuming processing is done externally)
        processed_image_url = image_url.replace("uploads", "processed")  # Simulating processing

        # Step 2: Upload the processed image to Shopify Files
        shopify_image_url = upload_image_to_shopify(processed_image_url)

        if not shopify_image_url:
            return jsonify({"error": "Failed to upload image to Shopify"}), 500

        # Step 3: Update Shopify order metafield
        metafield_response = update_shopify_order_metafield(order_id, shopify_image_url)

        return jsonify({
            "original_image": image_url,
            "processed_image_url": processed_image_url,
            "shopify_image_url": shopify_image_url,
            "shopify_response": metafield_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
