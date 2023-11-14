import urllib.request
import re
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from calculate_v3 import calculate_v3

app = Flask(__name__)
CORS(app)


# Define df and extract_mass_excess at the global level
df = None



if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
    #check if the server is running
    print("Server is running!")

