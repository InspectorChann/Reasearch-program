import math

'''
def saturation_vapor_pressure_at(db_T):
	P = math.exp(18.6686 - 4030.183 / (db_T + 235.0))
	return P
	'''
def saturation_vapor_pressure_at(db_T):
	P = 0.75006*6.11*(10**((7.5*db_T)/(237.3+db_T)))
	return P