import math

def saturation_vapor_pressure_at(db_T):
	P = math.exp(18.6686 - 4030.183 / (db_T + 235.0))
	return P