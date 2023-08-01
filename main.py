from flask import Flask, jsonify, request
from flask_cors import CORS
from data_utils import read_nuclear_mass_table
from calculations import calculate_v3, calculate_nuclear_mass

app = Flask(__name__)
CORS(app)

# Load the nuclear mass data table
nuclear_mass_df = read_nuclear_mass_table()


# Route for calculating nuclear mass values
@app.route('/calculate_mass_excess', methods=['POST'])
def doCalculations():
    """
    Calculate nuclear mass values for the specified particles.

    Request Format:
    {
        "particles": [
            {"a": 1, "z": 1, "particle": "H-1"},
            {"a": 2, "z": 1, "particle": "H-2"},
            ...
        ]
    }

    Response Format:
    {
        "H-1": 1.007825,
        "H-2": 2.014102,
        ...
    }
    """
    return calculate_nuclear_mass()


# Route for calculating the velocity of the third particle
@app.route('/calculate_v3', methods=['POST'])
def doCalculationsforV3():
    """
    Calculate the velocity of the third particle in a nuclear reaction.

    Request Format:
    {
        "mass1": 1.007825,
        "mass2": 2.014102,
        "mass3": 3.016049,
        "E_x": 2,   # Excitation energy in MeV
        "T_1": 5    # Kinetic energy of the first particle in MeV
    }

    Response Format:
    {
        "v3": 0.228143
    }
    """
    data = request.get_json()
    result = calculate_v3(
        m1=data['mass1'], 
        m2=data['mass2'], 
        m3=data['mass3'], 
        E_x=data['E_x'], 
        T_1=data['T_1']
        )
    return jsonify(result)



if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
    
