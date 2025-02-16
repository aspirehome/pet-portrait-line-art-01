import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load credentials from environment variables
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_ADMIN_API_KEY = os.getenv("SHOPIFY_ADMIN_API_KEY")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2023-10")

# Function to update Shopify order metafield
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
    print("Shopify Metafield Update Response:", response.json())  # Debug log
    return response.json()

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        image_url = data.get("image_url")
        order_id = data.get("order_id")  # Shopify order ID

        if not image_url or not order_id:
            return jsonify({"error": "Missing image_url or order_id"}), 400

        # Simulated image processing (Replace with actual logic)
        processed_image_url = image_url.replace("uploads", "processed")  # Dummy processing logic

        # Save processed image URL to Shopify Order Metafield
        shopify_response = update_shopify_order_metafield(order_id, processed_image_url)

        return jsonify({
            "original_image": image_url,
            "processed_image_url": processed_image_url,
            "shopify_response": shopify_response,
            "status": "success"
        })
    
    except Exception as e:
        print("Error:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
