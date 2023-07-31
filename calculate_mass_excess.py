from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import urllib.request
import re
import math

app = Flask(__name__)
CORS(app)

# Constants for neutron and proton masses in MeV/c^2
neutron_mass_MeV = 939.565
proton_mass_MeV = 938.272


#READING THE TABLE FROM THE WEBSITE
def read_table():
    url = "https://www.anl.gov/sites/www/files/2021-05/mass_1.mas20.txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    lines = data.splitlines()[36:]
    columns_with_numbers = []
    N_values = []
    A_values = []
    mass_excess_values = []
    Z_values = []
    nuclear_mass = []
    for line in lines:
        if not line.strip():
            continue
        
        if line.startswith('0'):
            line = line[1:]
        
        columns = re.findall(r"[-+]?[\d.]+(?:[eE][-+]?\d+)?", line)
        columns_with_numbers.append([float(column) for column in columns])
        N_values.append(int(columns[1]))
        Z_values.append(int(columns[2]))
        A_values.append(int(columns[3]))
        mass_excess_values.append(float(columns[4]))
        nuclear_mass_value = Z_values[-1] * proton_mass_MeV + N_values[-1] * neutron_mass_MeV + mass_excess_values[-1]
        nuclear_mass.append(nuclear_mass_value)

    data = {
        'A': A_values,
        'N': N_values,
        'Mass Excess': mass_excess_values,
        'Z': Z_values,
        'Nuclear Mass': nuclear_mass
    }
    df = pd.DataFrame(data)
    return df


df = read_table()

#EXTRACTING THE NUCLEAR MASS VALUES FROM THE TABLE

def extract_nuclear_mass(df, N, Z):
    filtered_df = df.loc[(df['A'] == Z) & (df['N'] == N), 'Nuclear Mass']
    
    if filtered_df.empty:
        return None  # or some other placeholder/error message
    
    return filtered_df.values[0]


#CALCULATE THE NUCLEAR MASS VALUES

def calculate_nuclear_mass():
    data = request.get_json()
    nuclear_mass_values = {}

    print(data)

    for particle in data:
        A = int(particle['a'])
        N = int(particle['z'])
        nuclear_mass = extract_nuclear_mass(df, A, N)
        
        # Handle potential None value
        if nuclear_mass is None:
            nuclear_mass_values[particle['particle']] = "Data not found"
        else:
            nuclear_mass_values[particle['particle']] = nuclear_mass

    return jsonify(nuclear_mass_values)


def calculate_v3(m1, m2, m3, E_x, T_1):
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    E_x = int(E_x)
    T_1 = int(T_1)
    print("DATA: ", m1, m2, m3, E_x, T_1)
    T_i = (m2 / (m1 + m2)) * T_1
    Q = (m1 + m2) - (m3 + m1)
    numerator = 2 * m1 * (T_i + Q - E_x)
    denominator = m3 * (m3 + m1)
    v3 = math.sqrt(abs(numerator) / abs(denominator))
    return v3
