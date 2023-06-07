
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

# NEXT STEPS
# iterate through all fields
# Make a deep copy of the parent struct
# for each range / enum attribute
# Set the field
# Save the data to a file

# After that we need to disable the validation, 
# and set the ranges outside of the valid range.

# More context
# Health will be initalized with valid data initally
# We will modify it to become invalid on a per parameter basis 

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
