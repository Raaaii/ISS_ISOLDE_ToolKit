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


def calculate_v3(m1, m2, m3, E_x, T_1):
    """
    Calculate the velocity of the third particle in a nuclear reaction.

    Parameters:
        - m1 (float): Mass of the first particle in MeV/c^2.
        - m2 (float): Mass of the second particle in MeV/c^2.
        - m3 (float): Mass of the third particle in MeV/c^2.
        - E_x (int): Excitation energy in MeV.
        - T_1 (int): Kinetic energy of the first particle in MeV.

    Returns:
        The velocity of the third particle in units of the speed of light (c).
    """
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    E_x = int(E_x)
    T_1 = int(T_1)
    T_i = (m2 / (m1 + m2)) * T_1
    Q = (m1 + m2) - (m3 + m1)
    numerator = 2 * m1 * (T_i + Q - E_x)
    denominator = m3 * (m3 + m1)
    v3 = math.sqrt(abs(numerator) / abs(denominator))
    return v3
