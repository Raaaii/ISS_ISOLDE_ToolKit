from flask import Flask, jsonify, request
from flask_cors import CORS
from data_utils import read_nuclear_mass_table
from calculations import calculate_v3, calculate_nuclear_mass, calculate_m4, given_z_find_theta, find_optimal_theta
import math
from data_utils import read_nuclear_mass_table

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


df = read_nuclear_mass_table()
df.reset_index(drop=True, inplace=True)


# Calculate the mass of the fourth particle

@app.route('/calculate_m4', methods=['POST'])
def doCalculationsforM4():
    """
    Calculate the mass of the fourth particle.

    Request Format:
    {
        "particles": [
            {"a": 1, "z": 1, "particle": "H-1"},
            {"a": 2, "z": 1, "particle": "H-2"},
            {"a": 3, "z": 2, "particle": "He-3"},
            ...
        ]
    }

    Response Format:
    {
        "Particle 4": 4.002603
    }
    """
    data = request.get_json()
    print("Received data:", data)  # Debug print
    result = calculate_m4(data['particles'])  # Call the modified calculate_m4 function
    response = {"Particle 4": result}
    print("Sending response:", response)  # Debug print
    return jsonify(response)




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
        m4=data['mass4'],
        E_x=data['E_x'], 
        T_1=data['T_1']
        )
    return jsonify(result)



@app.route("/given_z_find_theta", methods=['POST'])  # Change the URL to match your endpoint

def doCalculationsGivenZtoTheta():

    data = request.get_json()
    result = given_z_find_theta(
        m1=data['mass1'],
        m2=data['mass2'],
        m3=data['mass3'],
        m4=data['mass4'],
        v_3=data['v_3'],
        T_1=data['T_1'],
        z=data['z'],
        #q is 1.6*10^-19
        B_value=data['B_value']
    )

    print(result)
    return jsonify(result)

#Route to calculate optimal theta values 
@app.route('/find_optimal_theta', methods=['POST'])
def doCalculationsforOptimalTheta():


    data = request.get_json()
    result = find_optimal_theta(
        m_1=data['mass1'],
        m_2=data['mass2'],
        m_3=data['mass3'],
        m_4=data['mass4'],
        v_3=data['v_3'],
        T_1=data['T_1'],

        z_meas=data['z_meas'],
        ro_measured1=data['ro_measured1'],
        ro_measured2=data['ro_measured2'],
        B_value=data['B_value']
    )

    print(result)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
    
