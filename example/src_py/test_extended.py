
import ectypes_gps as gps
#import pytest

import copy as cpy
import importlib
import inspect
import ctypes
 

health = gps.Health_M()
health.dac = 11.9

try:
  health.dac = 10
  print("Failure , not caught")
except:
  print("Exception caught")
  
print(health.dac)

#make a deep copy of the parent struct
parentStructCopy=cpy.deepcopy(health) 

file_counter = 0
for f in health._efields_:
  
  fname = f[0]
  fpart = f[1]
  print(fname, fpart.range)
  if fpart.range:
    # TODO somehow disable validation  check...
    setattr(health, fname, fpart.range[0] )
    with open(f'{type(health).__name__}_{file_counter}.bin', 'wb') as fid:
      fid.write(health)
      file_counter += 1



print('\n', '\n')
print("scanning python modules for command/telemetry data...")
print('\n', '\n')


"""
module1 = importlib.import_module('tlm_dictonary')

print("dir is: ", dir(module1), '\n')

command_telem_data = [func for func in dir(module1) if callable(getattr(module1, func)) and type(getattr(module1, func)(ctypes.Structure))==ctypes.Structure]
"""


#scan tlm_dictionary for ctypes
#import ectypes_gps.py
module1 = importlib.import_module('ectypes_gps')

ectypesCtypesScan = []

for name, obj in inspect.getmembers(module1):
    if hasattr(obj, '_tlm_'):
       print("TLM/CMD data: ", obj, "\n\n")
       ectypesCtypesScan.append(obj)

print("cTypes for CMD/TLM in ectypes_gps are: ", ectypesCtypesScan)

print('\n', '\n')