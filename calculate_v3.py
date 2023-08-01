import math
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS


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
