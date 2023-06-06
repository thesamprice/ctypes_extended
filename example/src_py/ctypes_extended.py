
import ctypes


_StructureType = type(ctypes.Structure)
_BEStructureType = type(ctypes.BigEndianStructure)
_LEStructureType = type(ctypes.LittleEndianStructure)

def _repr_wrapper(value, transform):
    class ReprWrapper(type(value)):
        def __new__(cls, value):
            return super().__new__(cls, value)
        def __repr__(self):
            return transform(self)

    return ReprWrapper(value)


def _help_wrapper(field):
    class Field2(field.__class__):
        __doc__ = field.help

        def __repr__(self):
            return self.__doc__

    return Field2(field.name, field.type_, help=field.help, repr=field.repr, enum=field.enum)


class _Field:
    def __init__(self, name, type_, **kwargs):
        self.name = name
        self.type_ = type_
        self.real_name = "_" + name
        self.maxRange = 10
        self.minRange = 5
        self.help = kwargs.pop("description", f"Proxy structure field {name}")
        self.repr = kwargs.pop("repr", None)
        self.enum = kwargs.pop("enum", None)
        self.unit = kwargs.pop("unit", None)
        self.default = kwargs.pop("default", None)
        if self.enum:
            self.rev_enum =  {constant.value:constant for constant in self.enum.__members__.values() }
            if not 0 in self.rev_enum and not self.default:
                self.default = list(self.rev_enum.values())[0].value
    def __get__(self, instance, owner):
        if not instance:
            return _help_wrapper(self)

        value = getattr(instance, self.real_name)
        if self.enum:
            if value in self.rev_enum:
                return self.rev_enum[value]
            else:
                value = list(self.rev_enum.values())[0]
                setattr(instance, self.real_name, value.value)
                return value
        if self.repr:
            return _repr_wrapper(value, self.repr)

        return value

    def __set__(self, instance, value):
        print("now printing val: ", value)
        print("now printing minRange: ", self.minRange)
        print("now printing maxRange: ", self.maxRange)
        
        rangeArray = [self.minRange, self.maxRange]

        print ("rangeArray is", rangeArray)

        if value and value not in rangeArray:
            raise ValueError('value to set is outside of range')

        if self.enum:
            if(type(value) is str):
                value = self.enum[value].value
            else:
                value = getattr(self.enum, value.name).value
        setattr(instance, self.real_name, value)

def _ExtendedStructureMetaInitFields(namespace):
    _fields = namespace.get("_fields_", "")
    classic_fields  = []
    extended_fields = []
    default_fields = []
    for field in _fields:
        # Create the set of descriptors for the new-style fields:
        name = field[0]
        c_type = field[1]
        c_dict = field[2] if len(field) > 2 else {}
        namespace[name] = _Field(name, c_type, **(c_dict))
        extended_fields.append( (name, namespace[name]))
        if namespace[name].default:
            default_fields.append (("_" + name, namespace[name].default))
        if 'bits' in c_dict:
            classic_fields.append(("_" + name, field[1], c_dict['bits']))
        else:
            classic_fields.append(("_" + name, field[1]))

    namespace["_fields_"] = classic_fields
    namespace["_efields_"] = extended_fields
    namespace["_default_fields"] = default_fields



class _ExtendedStructureMeta(_StructureType):
    def __new__(metacls, name, bases, namespace):
        _ExtendedStructureMetaInitFields(namespace)
        return super().__new__(metacls, name, bases, namespace)


class _BigEndianExtendedStructureMeta(_BEStructureType):
    def __new__(metacls, name, bases, namespace):
        _ExtendedStructureMetaInitFields(namespace)
        return super().__new__(metacls, name, bases, namespace)


class _LittleEndianExtendedStructureMeta(_LEStructureType):
    def __new__(metacls, name, bases, namespace):
        _ExtendedStructureMetaInitFields(namespace)
        return super().__new__(metacls, name, bases, namespace)




class ExtendedStructure(ctypes.Structure, metaclass=_ExtendedStructureMeta):
    __slots__ = ()
    def __init__(self):
        for field in self._default_fields:
            setattr(self,field[0],field[1])
        print("meta init",self._fields_) 
        return super().__init__() 


class BigEndianExtendedStructure(ctypes.BigEndianStructure, metaclass=_BigEndianExtendedStructureMeta):
    __slots__ = ()


class LittleEndianExtendedStructure(ctypes.LittleEndianStructure, metaclass=_LittleEndianExtendedStructureMeta):
    __slots__ = ()

