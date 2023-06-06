import ctypes_extended
import ctypes
import warnings
#run `pip install enum34` if your getting a failure on the next line
import enum
import os
import sys

# lib_file = "gps"
# ext = {'darwin':'dylib','linux2':'so','linux':'so','win32':'dll'}
# lib_file += '.' + ext[sys.platform]

# path = os.path.dirname(__file__)
# lib_file = os.path.join(path, lib_file)

# gps = ctypes.CDLL(lib_file)

class app_apids(enum.Enum):
    GPS_Cmd_M_ID = 0
    Health_M_ID  = 1
    Pos_M_ID     = 2

class CordFrame(enum.Enum):
    ECEF    = 1
    J2K     = 2
    LATLONG = 3

class CCSDS_CMD_TLM(enum.Enum):
    TLM = 0
    CMD = 1

class NOISE_MODELS(enum.Enum):
    LINEAR     = 0
    POLYNOMIAL = 1
    WAVEFORM   = 2

class CCSDS_PriHdr_t_StreamId (ctypes_extended.BigEndianExtendedStructure):
    """CCSDS Stream id"""
    _pack_ = 1
    _fields_ = [ 
                ("packet_version_number"    , ctypes.c_uint16 ,
                    {"bits":3, 
                    "default":0,
                    }
                ),
                ("packet_type"              , ctypes.c_uint16 ,
                    {"bits":1,
                    "enum":CCSDS_CMD_TLM
                    }
                ),
                ("secondary_header_present" , ctypes.c_uint16 ,
                    {
                    "bits":1,
                    "type":bool,
                    "description":"""The Secondary Header Flag shall indicate the presence or absence of the Packet Secondary Header within this Space Packet.
It shall be 1 if a Packet Secondary Header is present; it shall be 0 if a Packet Secondary Header is not present.
"""
                    }  
                ),
                ("apid", ctypes.c_uint16 ,
                    {"bits":11,
                        "description":"""via 135.0-b-1 application ID's 2040- 2047 are reserved and should not be used.
The APID (possibly in conjunction with the optional APID Qualifier that
identifies the naming domain for the APID) shall provide the naming mechanism for the LDP."""
                    }
                ),
                 ]


class CCSDS_PriHdr_t_Sequence (ctypes_extended.BigEndianExtendedStructure):
    """CCSDS Sequence ID"""
    _pack_ = 1
    _fields_ = [ ("sequence_flags" , ctypes.c_uint16 ,
                    {"bits":2,
                    "default":3,
                    "description":"3 = complete packet"
                    }
                ),
                 ("sequence_count" , ctypes.c_uint16 ,
                    {
                     "bits":14,
                     "description": "Packet sequence counter"
                    } 
                 ),
               ]


class CCSDS_PriHdr_t (ctypes_extended.BigEndianExtendedStructure):
    """CCSDS Header"""
    _pack_ = 1
    _fields_ = [ ("StreamId" , CCSDS_PriHdr_t_StreamId ),
                 ("Sequence" , CCSDS_PriHdr_t_Sequence ),
                 ("Length"   , ctypes.c_uint16 ,
                    {"description":"The Packet data length. Total number of octets in packet data field - 1"
                    }
                 )]
    #TODO unsure how best to implement this.
    def init(self):
        self.Length = self._parent._size - 6 - 1


def voltage_validator(self,value):
    if value< 11.8:
        raise ValueError("volatage min error")
    if value > 12.2:
        raise ValueError("volatage min error")
def voltSet(self,value):
    """converts a float to a int16
    voltage is assumed to be between 0 and 20v
    """
    self._raw = int(value/20.0* (2**16))

def voltGet(self):
    """converts a int16  to a float
    voltage is assumed to be between 0 and 20v
    """
    return self._raw * (2**16)/20.0


class Health_M (ctypes_extended.ExtendedStructure):
    """/*!
* @brief Packet health
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid Health_M_ID
*/
Health_M{
    /*!
    * @bigendian
    * @const StreamId.packet_type CCSDS_TLM
    * @const StreamId.apid Health_M_ID
    * @const StreamId.packet_version_number 3
    */
    CCSDS_PriHdr_t header;
    /*!
    * @unit volts
    * @range [11.8, 12.2]
    */
    float voltage;

    /*!
    * @unit volts
    * @range [11.8,12.2]
    * @brief Digital to analog controller from DAC
    * @setter VoltConverter
    */
   int16_t dac;

"""

    
    ids = {"header.StreamId.packet_type":CCSDS_CMD_TLM.TLM,
           "header.StreamId.apid":app_apids.Health_M_ID,
           "header.StreamId.packet_version_number":3
          }
    _pack_ = 1
    _apid_ = 1
    _tlm_  = 1
    _fields_ = [ ("header"         , CCSDS_PriHdr_t     ),
                 ("Padding_48_64_" , ctypes.c_ubyte * 2,
                     {"hidden":True}
                  ),
                 ("voltage"        , ctypes.c_float,
                    {
                     "unit":"volts",
                     "validator":voltage_validator
                    }     
                 ),
                 ("dac"            , ctypes.c_int16,
                    {
                        "description":"Digital to analog controller from DAC",
                        "setter":voltSet,
                        "getter":voltGet,
                        "validator":voltage_validator
                    }
                 ),
                 ("minRange"            , ctypes.c_int16,
                    {
                        "description":"minimum possible voltage",
                        "unit":"volts"
                    }
                 ),
                 ("maxRange"            , ctypes.c_int16,
                    {
                        "description":"maximum possible voltage",
                        "unit":"volts"
                    }
                 ),
                 ("Padding_112_"   , ctypes.c_ubyte * 2,
                    {"hidden":True}
                 )]
    minRange = 11.8
    maxRange = 12.2

class Pos_M (ctypes_extended.ExtendedStructure):
    """GPS packet describing position info"""
    ids = {
        "header.StreamId.apid":app_apids.Pos_M_ID,
        }
    
    _pack_ = 1
    _apid_ = 2
    _tlm_  = 1
    _fields_ = [ ("header"         , CCSDS_PriHdr_t,
                {
                    "field_overrides":{
                        "StreamId.packet_type":{
                            "default":CCSDS_CMD_TLM.TLM
                        },
                        "StreamId.packet_version_number":{
                            "default":3
                        }
                    }
                }      
            ),
                 ("Padding_48_64_" , ctypes.c_ubyte  * 2,
                    {"hidden":True,
                 } ),
                 ("pos"            , ctypes.c_double * 3,
                     {"unit":"meters",
                     "description":"position information in meters"
                     } 
                 ),
                 ("_padding"       , ctypes.c_ubyte,
                    {"hidden":True}
                 ),
                 ("coord_frame"    , ctypes.c_ubyte,
                 {
                     "description":"Coordinate system that field pos applies to",
                     "enum":CordFrame
                 }),
                 ("Padding_272_"   , ctypes.c_ubyte  * 6,
                    {"hidden":True
                    } 
                 )]


class ModelLinear (ctypes_extended.ExtendedStructure):
    """/*!
* @brief describes y=x*slope + const
*/
ModelLinear
{
    /*!
    * @brief constant
    */
    double cons;
    /*!
    * @brief slope
    */
    double slope;
"""
    _pack_ = 1
    _fields_ = [ ("cons"  , ctypes.c_double ),
                 ("slope" , ctypes.c_double )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class ModelPolynomial (ctypes_extended.ExtendedStructure):
    """/*!
* @brief describes y=x_0 + x_1*x + x_2*x*x
*/
ModelPolynomial
{
    double x_0;
    double x_1;
    double x_2;

"""
    _pack_ = 1
    _fields_ = [ ("x_0" , ctypes.c_double ),
                 ("x_1" , ctypes.c_double ),
                 ("x_2" , ctypes.c_double )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class ModelWaveform (ctypes_extended.ExtendedStructure):
    """/*!
* @brief describes y=a*sin(x) + b*cos(x)
*/
ModelWaveform
{
    double a;
    double b;

"""
    _pack_ = 1
    _fields_ = [ ("a" , ctypes.c_double ),
                 ("b" , ctypes.c_double )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


def modelSetter(self,value):
    "Example of changing parent attributes on set"
    self._parent.linear.disabled   = False
    self._parent.poly.disabled     = False
    self._parent.waveform.disabled = False

    if value != NOISE_MODELS.LINEAR:
        self._parent.linear.disabled = True
    if value != NOISE_MODELS.POLYNOMIAL:
        self._parent.poly.disabled = True
    if value != NOISE_MODELS.WAVEFORM:
        self._parent.waveform.disabled = True
    self._raw = value
class GPS_Cmd_M (ctypes_extended.ExtendedStructure):
    """Command to set noise model"""
    _pack_ = 1
    _apid_ = 0
    _tlm_  = 1
    _fields_ = [ ("header"          , CCSDS_PriHdr_t,
                {
                    "field_overrides":{
                        "StreamId.packet_type":{
                            "default":CCSDS_CMD_TLM.CMD
                        },
                        "StreamId.packet_version_number":{
                            "default":3
                        }
                    }
                }
                 ),
                 ("Padding_48_64_"  , ctypes.c_ubyte * 2,
                    {"hidden":True}
                  ),
                 ("noise_model"     , ctypes.c_int32,
                    {"enum":NOISE_MODELS,
                    "setter":modelSetter,
                    "description":"""Describes the fit model to use, and its parameters"""
                    }     
                 ),
                 ("Padding_96_128_" , ctypes.c_ubyte * 4,{"hidden":True} ),
                 ("linear"          , ModelLinear        ),
                 ("poly"            , ModelPolynomial    ),
                 ("waveform"        , ModelWaveform      )]


