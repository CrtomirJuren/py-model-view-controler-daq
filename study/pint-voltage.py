# import pint

from pint import UnitRegistry
ur = UnitRegistry()

# current = 5 * ur.ampere
current = 5000 * ur.mA
resistance = 10 * ur.ohm
# U = R*I
voltage = current * resistance

# voltage = voltage.to(ur.volt)
voltage = voltage.to('volt')
print(voltage, ' = ', current, ' * ', resistance)
