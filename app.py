from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Pet Portrait Line Art API is running!'

# ✅ Add the missing /process route
@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    
    if not data or 'image_url' not in data:
        return jsonify({"error": "No image URL provided"}), 400

    image_url = data['image_url']
    
    # 🔹 Mock response (Replace with actual processing later)
    processed_image_url = f"https://yourstorage.com/processed-{image_url.split('/')[-1]}"
    
    return jsonify({
        "status": "success",
        "original_image": image_url,
        "processed_image_url": processed_image_url
    })

if __name__ == '__main__':
    app.run(debug=True)

