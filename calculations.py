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
    a1=float(data[0]['a'])
    z1=float(data[0]['z'])
    a2=float(data[1]['a'])
    z2=float(data[1]['z'])
    a3=float(data[2]['a'])
    z3=float(data[2]['z'])
    # print("PODACIIIIII: ", float(data[0]['a']), float(data[0]['z']), float(data[1]['a']), float(data[1]['z']), float(data[2]['a']), float(data[2]['z']))
    m4 = calculate_m4(float(data[0]['a']), float(data[0]['z']), float(data[1]['a']), float(data[1]['z']), float(data[2]['a']), float(data[2]['z']), df)
    nuclear_mass_values['Particle 4'] = m4
    print("M4 jE: ================================= ", m4)
    return jsonify(nuclear_mass_values)



# Constants for neutron and proton masses in MeV/c^2
NEUTRON_MASS_MEV = 939.565

PROTON_MASS_MEV = 938.272

def calculate_m4(a1,z1,a2,z2,a3,z3, df): # Calculate "a" and "z" values of the fourth particle
    z4 = z1 + z2 - z3
    a4 = a1 + a2 - a3
    filtered_df = df.query('A == @a4 & Z == @z4')

    if not filtered_df.empty:
        nuclear_mass_4 = filtered_df['Nuclear Mass'].iloc[0]
    else:
        nuclear_mass_4 = "Data not found"
    return nuclear_mass_4




#def calcuate_m4():
 #   data = request.get_json()
 #   m4_values = {}  # Create an empty dictionary to store mass values for each particle
    
 #   for particle in data:
 #       A = int(particle['a'])
 #       Z = int(particle['z'])
 #       A_4 = int(data[0]['a']) + int(data[1]['a']) - int(data[2]['a'])
 #       Z_4 = int(data[0]['z']) + int(data[1]['z']) - int(data[2]['z'])
        
 #       # Calculate the mass of the fourth particle
 #       m4 = (A_4 - Z_4) * NEUTRON_MASS_MEV + Z_4 * PROTON_MASS_MEV + df.query('A == @A_4 & Z == @Z_4')['Mass Excess'].iloc[0]
        
        # Store the calculated mass in the dictionary
  #      m4_values['Particle 4'] = m4

 #   return jsonify(m4_values)  # Return the dictionary with calculated mass values




def calculate_v3(m1, m2, m3,m4,  E_x, T_1):
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


#Calculate the velocity of the fourth particle in a nuclear reaction.



#Finding the optimal theta values. 

import math

import math

def given_z_find_theta(z_1, z_2, m1, m2, m3, m4, T_1, v_3, t_cyclotron):
    z_1 = float(z_1)
    z_2 = float(z_2)
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    m4 = float(m4)
    T_1 = float(T_1)
    v_3 = float(v_3)
    t_cyclotron = 1e-6

    V_i = math.sqrt(2 * T_1 * m1 / (m1 + m2))
    V_f = m1 + m2 / (m3 + m4) * V_i

    # Calculate the first theta_cm value for z_1
    v_parallel_1 = z_1 / t_cyclotron
    theta_cm_1 = math.acos((V_f - v_parallel_1) / v_3)

    # Calculate the second theta_cm value for z_2
    v_parallel_2 = z_2 / t_cyclotron
    theta_cm_2 = math.acos((V_f - v_parallel_2) / v_3)

    return theta_cm_1, theta_cm_2



                       



def find_optimal_theta(ro_meas1, ro_meas2, v_3, m_3, B, q, initial_theta_lab, tolerance=1e-6, max_iterations=100):
    B = float(B)
    q = float(q)
    m_3 = float(m_3)
    v_3 = float(v_3)
    ro_meas1 = float(ro_meas1)
    ro_meas2 = float(ro_meas2)
    initial_theta_lab = float(initial_theta_lab)
    tolerance = float(tolerance)
    max_iterations = int(max_iterations)

    theta_lab1 = initial_theta_lab
    theta_lab2 = initial_theta_lab

    z_mes1 = 2 * math.pi / B / q * m_3 * v_3 * math.cos(theta_lab1)
    z_mes2 = 2 * math.pi / B / q * m_3 * v_3 * math.cos(theta_lab2)

    for i in range(max_iterations):
        R1 = (m_3 * v_3 * math.sin(theta_lab1)) / (q * B)
        psi1 = 2 * math.asin(ro_meas1 / (2 * R1))

        numerator1 = (1 - (psi1 / (2 * math.pi))) * z_mes1 - z_mes1
        denominator1 = 1 - (psi1 / (2 * math.pi))
        z_next1 = z_mes1 - numerator1 / denominator1

        if abs(z_next1 - z_mes1) < tolerance:
            break

        z_mes1 = z_next1

    for i in range(max_iterations):
        R2 = (m_3 * v_3 * math.sin(theta_lab2)) / (q * B)
        psi2 = 2 * math.asin(ro_meas2 / (2 * R2))

        numerator2 = (1 - (psi2 / (2 * math.pi))) * z_mes2 - z_mes2
        denominator2 = 1 - (psi2 / (2 * math.pi))
        z_next2 = z_mes2 - numerator2 / denominator2

        if abs(z_next2 - z_mes2) < tolerance:
            break

        z_mes2 = z_next2

    theta_lab1 = math.acos((q * B * z_next1) / (2 * math.pi * m_3 * v_3))
    theta_lab2 = math.acos((q * B * z_next2) / (2 * math.pi * m_3 * v_3))

    theta_lab = theta_lab2 - theta_lab1

    #as output two angles. !!!!

    return theta_lab
