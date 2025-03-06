from flask import Flask, request, jsonify
import util

# Initialize Flask app
app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Endpoint to ge,.,...................................................................................................................................................................................... location names."""
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
    except Exception as e:
        response = jsonify({'error': str(e)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """Endpoint to predict home price based on input data."""
    try:
        # Validate incoming form data
        total_sqft = float(request.form.get('total_sqft', 0))
        location = request.form.get('location', '').strip()
        bhk = int(request.form.get('bhk', 0))
        bath = int(request.form.get('bath', 0))

        if not total_sqft or not location or bhk <= 0 or bath <= 0:
            raise ValueError("Invalid input data. Ensure all fields are filled correctly.")

        # Predict price
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
    except Exception as e:
        response = jsonify({'error': str(e)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.errorhandler(404)
def page_not_found(e):
    """Handle undefined routes."""
    return jsonify({'error': 'Endpoint not found. Check the URL and try again.'}), 404

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        util.load_saved_artifacts()
        app.run(debug=True)  # Enable debug mode for better error tracking during development
    except Exception as e:
        print(f"Error starting server: {e}")
