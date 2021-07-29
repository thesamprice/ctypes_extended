# ctypes_extended
This project aims to extend ctypes to support the following features.

- Attributes per field
- Attributes per struct
- Compatible with C callbacks as ctypes is.

It is primarly aimed at ccsds packets, but is hopefully general enough to be used for other applications.

## Struct attributes
- Description
- Anything else
  Gets mapped as a parameter, if function gets mapped as a callback. With self passed?

## Feild Attributes
### Field Attributes setable
- **Id**
  Defines a field in a C structure that can be used to identify that structure.
  
  In example 

  - A. a network packet might contain a unique set of bits that map to a specific structure.
  - B. Files often mark the first few bytes with magic numbers conforming to the packet type.
- **Hidden**
  Marks a field as hidden / not used.

  In example

    Padding bytes

  Field could be become hidden at runtime. Ie another bit is set marking this field as not used.

- **Endianness** (Might not be possible without whole struct marked as big/little endian)
  - Values: Big, Little
- **Unit**
  - String describing unit
  - Value string
- **Validator**
  Callback function, that can be used to validate the fields.

  In several systems there will be different errors.  Yellow limits, REd limits.  

  Would it make sense to have these be passed as different exception types?

  Ability to change validator on fly.  Validation ranges / routine could change at runtime.

- **Setter**
  Callback function, that can be used to convert the field when being set, self being passed.

- **Getter**
  Callback function, that can be used to convert the field when getting. self being passed

- **Enum**
  - Specifies an enum that this parameter maps to.

- **Description**
  - Description of field, used to populate help call

- **AnythingElse**
  Gets mapped as a parameter, if function gets mapped as a callback. With self passed?

### Field Attributes Not setable 
- **_raw**
  Provides raw binary value.
- **_parent**
  Gets set internally to parent.
- **_id**
  Unique ID, name it based off of "parent.child1.child2.child3"

