import pickle
import json
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())  # Ensure location matching is case-insensitive
    except ValueError:
        loc_index = -1  # If location not found, set index to -1

    # Prepare the feature vector
    x = np.zeros(len(__data_columns))  # Ensure the input vector matches the expected feature length
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:  # Set location feature to 1 if it exists
        x[loc_index] = 1

    # Make the prediction using the loaded model
    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    # Load data columns from JSON file
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]  # First 3 columns are sqft, bath, bhk

    # Load the trained model from the pickle file
    global __model
    if __model is None:
        with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")


def get_location_names():
    return __locations


def get_data_columns():
    return __data_columns


if __name__ == "__main__":
    # Load the saved artifacts
    load_saved_artifacts()

    # Test the model predictions
    print(get_location_names())  # Print all location names
    print(get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))  # Valid location
    print(get_estimated_price("1st Phase JP Nagar", 1000, 2, 2))  # Valid location
    print(get_estimated_price("Kalhalli", 1000, 2, 2))  # Unknown location
    print(get_estimated_price("Ejipura", 1000, 2, 2))  # Unknown location
