import math
from calculate_v3 import calculate_v3

def find_optimal_theta(ro_meas, v_3, m_3, B, q, initial_theta_lab, tolerance=1e-6, max_iterations=100):
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

ro_meas = 0.5
m_3 = 2.0
B = 1.0
q = 1.6e-19
initial_theta_lab = 0.1

# Call the calculate_v3 function from the v3_calculation.py file
v_3 = 1.0

optimal_theta_lab = find_optimal_theta(ro_meas, v_3, m_3, B, q, initial_theta_lab)
print(f"Optimal theta_lab: {optimal_theta_lab}")
