# ctypes_extended
This project aims to extend ctypes to support the following features.

- Attributes per field
- Attributes per struct
- Compatible with C function callbacks similar to ctypes.
- Ability to use reflection to autogenerate other language callbacks.

It is primarly aimed at ccsds packets, but is hopefully general enough to be used for other applications.

## Struct attributes
- **description** used to populate help call from python.
  Just use normal """ """ description ?

- **field_overrides**, array of dictionary of attributes to override on child fields.

- **ids** list of child parameters that are always constant, and their expected values.  Could be used by a telemetry processor. ie overlay struct on data buffer, and check to see if values match. Similar to field_overrides

- **validator** Callback function that throws errors if underlying data is bad?
  Unsure if this is a good idea.

- **hidden** boolean, default False

- **disabled** boolean, default False

- Anything else
  Gets mapped as a parameter, if function gets mapped as a callback. With self passed?
  Unsure if this is a good idea? Could manually just add functions?

### Struct Field Attributes Not setable 
- **_parent**
  returns the parent.
- **_id**
  Unique ID, name it based off of "parent.child1.child2.child3"
- **_size**
  ctypes size


## Feild Attributes
### Field Attributes setable
- **id**
  Defines a field in a C structure that can be used to identify that structure.
  
  In example 

  - A. a network packet might contain a unique set of bits that map to a specific structure.
  - B. Files often mark the first few bytes with magic numbers conforming to the packet type.
- **Hidden**
  Marks a field as hidden / not used.

  In example

    Padding bytes

  Field could be become hidden at runtime. Ie another bit is set marking this field as not used.

- **endianness** (Might not be possible without whole struct marked as big/little endian)
  - Values: Big, Little
  - Maybe force user to create packed structures around single elements.
- **unit**
  - String describing unit
  - Value string
  - example meters, seconds, radians
- **validator**
  Callback function, that can be used to validate the fields.

  In several systems there will be different errors.  Yellow limits, REd limits.  

  Would it make sense to have these be passed as different exception types?

  Ability to change validator on fly.  Validation ranges / routine could change at runtime.
- **type**
- **setter**
  Callback function, that can be used to convert the field when being set, self being passed.

- **getter**
  Callback function, that can be used to convert the field when getting. self being passed

- **enum**
  - Specifies an enum that this parameter maps to.

- **description**
  - Description of field, used to populate help call

- **AnythingElse**
  Gets mapped as a parameter, if function gets mapped as a callback. With self passed?

### Field Attributes Not setable 
- **_raw**
  Provides raw binary value.
- **_parent**
  returns the parent.
- **_id**
  Unique ID, name it based off of "parent.child1.child2.child3"
- **_size**
  ctypes size
