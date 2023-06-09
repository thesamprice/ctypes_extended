import copy as cpy
import ectypes_gps as gps
#import pytest
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

parentStructCopy=cpy.deepcopy(health) #make a deep copy of the parent struct 


#Write binary files for fuzzing
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


#scan tlm_dictionary for ctypes
module1 = importlib.import_module('tlm_dictonary')
tlmDictCtypesScan = []

for name, obj in inspect.getmembers(module1):
    if name.find('CType') != -1:
        tlmDictCtypesScan.append(name)
        #print(f'Found a ctypes structure: {name}')

print("the ctypes for command/telemetry in tlm_dictionary are: ", tlmDictCtypesScan)

print('\n', '\n')


#scan tlm_sqllite for ctypes
module2 = importlib.import_module('tlm_sqllite')
tlmSqlliteCtypesScan = []

for name, obj in inspect.getmembers(module2):
    if name.find('CType') != -1:
        tlmSqlliteCtypesScan.append(name)
        #print(f'Found a ctypes structure: {name}')

print("the ctypes for command/telemetry in tlm_sqllite are: ", tlmSqlliteCtypesScan)

print('\n', '\n') 

