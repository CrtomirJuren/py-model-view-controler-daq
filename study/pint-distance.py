import pint

ur = pint.UnitRegistry()
print(ur)
# meter = ur('meter')

visina = 1.78 * ur.m

print(visina)
print(type(visina))

visina_usa = visina.to(ur.inch)
print(visina_usa)

distance = 24.0 * ur.m
print('distance: ', distance)
# print(type(distance))
print('magnitude: ', distance.magnitude)
print('units: ', distance.units)

print('distance in km: ', distance.to(ur.km))