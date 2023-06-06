
import ectypes_gps as gps
#import pytest
 

health = gps.Health_M()
health.dac = 11.9

try:
  health.dac = 10
  print("Failure , not caught")
except:
  print("Exception caught")
  
print(health.dac)

for f in health._efields_:
  
  fname = f[0]
  fpart = f[1]
  print(fname, fpart.range)
  if fpart.range:
    # TODO somehow disable validation  check...
    setattr(health, fname, fpart.range[0] - 1)
    setattr(health, fname, fpart.range[1] + 1)