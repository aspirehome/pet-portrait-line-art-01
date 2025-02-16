import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Shopify API Credentials (Replace with actual values)
SHOPIFY_STORE_URL = "https://yourstore.myshopify.com"  # Replace with your actual store URL
SHOPIFY_ADMIN_API_KEY = "shpat_xxxxxxxxxxxxxxxxxxxxx"  # Replace with your actual API key
SHOPIFY_API_VERSION = "2023-10"  # Ensure this matches Shopify's latest API version

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
    return response.json()

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        image_url = data.get("image_url")
        order_id = data.get("order_id")  # Shopify order ID

        if not image_url or not order_id:
            return jsonify({"error": "Missing image_url or order_id"}), 400

        # Simulate image processing (Replace this with actual processing logic)
        processed_image_url = image_url.replace("uploads", "processed")  # Dummy example

        # Save processed image URL to Shopify Order Metafield
        shopify_response = update_shopify_order_metafield(order_id, processed_image_url)

        return jsonify({
            "original_image": image_url,
            "processed_image_url": processed_image_url,
            "shopify_response": shopify_response,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
