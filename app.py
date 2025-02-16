from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Pet Portrait Line Art API is running!'

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    image_url = data.get("image_url", "")

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    # Here, you would add your image processing logic
    return jsonify({"message": "Image received successfully", "image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)
