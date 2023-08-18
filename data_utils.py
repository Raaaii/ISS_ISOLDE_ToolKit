import pandas as pd
import urllib.request
import re

# Constants for neutron and proton masses in MeV/c^2
NEUTRON_MASS_MEV = 939.565
PROTON_MASS_MEV = 938.272


def read_nuclear_mass_table():
    """
    Read the nuclear mass data table from the website and return a DataFrame.

    Data Source: https://www.anl.gov/sites/www/files/2021-05/mass_1.mas20.txt
    """
    url = "https://www.anl.gov/sites/www/files/2021-05/mass_1.mas20.txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    lines = data.splitlines()[36:]
    columns_with_numbers = []
    N_values = []
    A_values = []
    mass_excess_values = []
    Z_values = []
    Binding_energy_values = []
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
        Binding_energy_values.append(float(columns[6]))
        nuclear_mass_value = Z_values[-1] * PROTON_MASS_MEV + N_values[-1] * NEUTRON_MASS_MEV - Binding_energy_values[-1]*A_values[-1]/1000
        nuclear_mass.append(nuclear_mass_value)

    data = {
        'A': A_values,
        'N': N_values,
        'Z': Z_values,
        'Binding Energy': Binding_energy_values,
        'Nuclear Mass': nuclear_mass
    }
    
    df = pd.DataFrame(data)
    return df

#df=read_nuclear_mass_table()
#print(df)
