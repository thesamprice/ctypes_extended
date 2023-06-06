
import ectypes_gps as gps
#import pytest
 

health = gps.Health_M()
health.dac = 11.9

try:

  health.dac = 10

except:
    raise ValueError('dac value outside of range')
