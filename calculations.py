import math
from flask import Flask, jsonify, request
from data_utils import read_nuclear_mass_table

df=read_nuclear_mass_table()
df.reset_index(drop=True, inplace=True)



def extract_nuclear_mass(df, A, Z):
    print("Z:", Z, "A:", A)
    filtered_df = df.query('A == @A & Z == @Z')
    print("Filtered DataFrame:", filtered_df)
    
    if filtered_df.empty:
        return None  # or some other placeholder/error message
    
    return filtered_df['Nuclear Mass'].iloc[0]



#filtered_df=extract_nuclear_mass(df, 1,2)
#print(filtered_df)


def calculate_nuclear_mass():


    """
    Calculate nuclear mass values for the specified particles.

    Parameters:
        - df (pandas.DataFrame): DataFrame containing the nuclear mass data table.
        - particles (list): List of dictionaries, each representing a particle with 'a' and 'z' values.

    Returns:
        A dictionary mapping particle names to their nuclear mass values.
    """
    data = request.get_json()
    nuclear_mass_values = {}

    print(data)

    for particle in data:
        A = int(particle['a'])
        Z = int(particle['z'])
        nuclear_mass = extract_nuclear_mass(df, A, Z)
        
        # Handle potential None value
        if nuclear_mass is None:
            nuclear_mass_values[particle['particle']] = "Data not found"
        else:
            nuclear_mass_values[particle['particle']] = nuclear_mass

    return jsonify(nuclear_mass_values)



# Constants for neutron and proton masses in MeV/c^2
NEUTRON_MASS_MEV = 939.565
PROTON_MASS_MEV = 938.272


def calcuate_m4():
    data = request.get_json()
    m4_values = {}  # Create an empty dictionary to store mass values for each particle
    
    for particle in data:
        A = int(particle['a'])
        Z = int(particle['z'])
        A_4 = int(data[0]['a']) + int(data[1]['a']) - int(data[2]['a'])
        Z_4 = int(data[0]['z']) + int(data[1]['z']) - int(data[2]['z'])
        
        # Calculate the mass of the fourth particle
        m4 = (A_4 - Z_4) * NEUTRON_MASS_MEV + Z_4 * PROTON_MASS_MEV + df.query('A == @A_4 & Z == @Z_4')['Mass Excess'].iloc[0]
        
        # Store the calculated mass in the dictionary
        m4_values['Particle 4'] = m4

    return jsonify(m4_values)  # Return the dictionary with calculated mass values




def calculate_v3(m1, m2, m3, m4, E_x, T_1):
    """
    Calculate the velocity of the third particle in a nuclear reaction.

    Parameters:
        - m1 (float): Mass of the first particle in MeV/c^2.
        - m2 (float): Mass of the second particle in MeV/c^2.
        - m3 (float): Mass of the third particle in MeV/c^2.
        - E_x (float): Excitation energy in MeV.
        - T_1 (float): Kinetic energy of the first particle in MeV.

    Returns:
        The velocity of the third particle in units of the speed of light (c).
    """
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    E_x = float(E_x)
    T_1 = float(T_1)
    T_i = (m2 / (m1 + m2)) * T_1
    Q = (m1 + m2) - (m3 + m4)
    numerator = 2 * m1 * (T_i + Q - E_x)
    denominator = m3 * (m3 + m1)
    v3 = math.sqrt(abs(numerator) / abs(denominator))
    return v3


#Finding the optimal theta values. 

def find_optimal_theta(ro_meas, v_3, m_3, B, q, initial_theta_lab, tolerance=1e-6, max_iterations=100):


    B=float(B)
    q=float(q)
    m_3=float(m_3)
    v_3=float(v_3)
    ro_meas=float(ro_meas)
    initial_theta_lab=float(initial_theta_lab)
    tolerance=float(tolerance)
    max_iterations=int(max_iterations)

    
    theta_lab = initial_theta_lab
    z_mes = 2 * math.pi /B /q * m_3 * v_3 * math.cos(theta_lab)

    for i in range(max_iterations):
        R = (m_3 * v_3 * math.sin(theta_lab)) / (q * B)  # Calculate R based on the current theta_lab
        psi = 2 * math.asin(ro_meas / (2 * R))  # Calculate psi using the current theta_lab and ro_meas

        numerator = (1 - (psi / (2 * math.pi))) * z_mes - z_mes
        denominator = 1 - (psi / (2 * math.pi))
        z_next = z_mes - numerator / denominator

        if abs(z_next - z_mes) < tolerance:
            break  # Stop iterating if z converges within the tolerance

        z_mes = z_next

    theta_lab = math.acos((q * B * z_next) / (2 * math.pi * m_3 * v_3))
    return theta_lab
