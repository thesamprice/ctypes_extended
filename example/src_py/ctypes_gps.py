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

class NOISE_MODELS(enum.Enum):
    LINEAR     = 0
    POLYNOMIAL = 1
    WAVEFORM   = 2

class CCSDS_PriHdr_t_StreamId (ctypes.BigEndianStructure):
    """"""
    _pack_ = 1
    _fields_ = [ 
                ("packet_version_number"    , ctypes.c_uint16 ,3  ),
                ("packet_type"              , ctypes.c_uint16 ,1  ),
                ("secondary_header_present" , ctypes.c_uint16 ,1  ),
                ("apid"                     , ctypes.c_uint16 ,11 ),
                 ]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class CCSDS_PriHdr_t_Sequence (ctypes.BigEndianStructure):
    """"""
    _pack_ = 1
    _fields_ = [ ("sequence_flags" , ctypes.c_uint16 ,2  ),
                 ("sequence_count" , ctypes.c_uint16 ,14 ),
               ]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class CCSDS_PriHdr_t (ctypes.BigEndianStructure):
    """/*!
* @bigendian
*/
CCSDS_PriHdr_t{
    /*!
    *@bitarray msbf
    *  @bits 3
    *    @name packet_version_number
    *    @brief Pacet Version Number
    *    @default 0
    *  @bits 1
    *    @name packet_type
    *    @brief Packet type
    *    @enum CCSDS_CMD_TLM
    *  @bits 1
    *    @name secondary_header_present
    *    @brief Secondary Header flag
    *    @detailed The Secondary Header Flag shall indicate the presence or absence of the Packet Secondary Header within this Space Packet.
    *    It shall be 1 if a Packet Secondary Header is present; it shall be 0 if a Packet Secondary Header is not present.
    *    @enum TRUE_FALSE
    *  @bits 11
    *    @name apid
    *    @brief Application Process Identifier (APID)
    *    @detailed  via 135.0-b-1 application ID's 2040- 2047 are reserved and should not be used.
    *    The APID (possibly in conjunction with the optional APID Qualifier that
    *    identifies the naming domain for the APID) shall provide the naming mechanism for the LDP.
    */
   uint16_t  StreamId;

   /*!
   *@bitarray msbf
   *  @bits 2
   *    @name sequence_flags
   *    @brief 3 = complete packet
   *  @bits 14
   *    @name sequence_count
   *    @brief  Packet Sequence Count
   */
   uint16_t  Sequence; 

   /*!
    * @brief The Packet data length. Total number of octets in packet data field - 1
    * @packetSize
    */
   uint16_t  Length;
"""
    _pack_ = 1
    _fields_ = [ ("StreamId" , CCSDS_PriHdr_t_StreamId ),
                 ("Sequence" , CCSDS_PriHdr_t_Sequence ),
                 ("Length"   , ctypes.c_uint16         )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class Health_M (ctypes.Structure):
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
    * @converter VoltConverter
    */
   int16_t dac;

"""
    _pack_ = 1
    _apid_ = 1
    _tlm_  = 1
    _fields_ = [ ("header"         , CCSDS_PriHdr_t     ),
                 ("Padding_48_64_" , ctypes.c_ubyte * 2 ),
                 ("voltage"        , ctypes.c_float     ),
                 ("dac"            , ctypes.c_int16     ),
                 ("Padding_112_"   , ctypes.c_ubyte * 2 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        self.header.StreamId.packet_type = 0
        self.header.StreamId.apid = 1
        self.header.StreamId.packet_version_number = 3


class Pos_M (ctypes.Structure):
    """/*!
* @brief GPS packet describing position info
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid Pos_M_ID
*/
Pos_M{
    /*!
    * @bigendian
    * @const StreamId.packet_type CCSDS_TLM
    * @const StreamId.apid Pos_M_ID
    * @const StreamId.packet_version_number 3
    */
    CCSDS_PriHdr_t header;

    /*!
    * @unit meters
    * @brief position information in meters
    */
    double pos[3];

    /*!
    * @hidden
    */
    uint8_t _padding;

    /*!
    * @enum CordFrame
    */
    uint8_t coord_frame;

"""
    _pack_ = 1
    _apid_ = 2
    _tlm_  = 1
    _fields_ = [ ("header"         , CCSDS_PriHdr_t      ),
                 ("Padding_48_64_" , ctypes.c_ubyte  * 2 ),
                 ("pos"            , ctypes.c_double * 3 ),
                 ("_padding"       , ctypes.c_ubyte      ),
                 ("coord_frame"    , ctypes.c_ubyte      ),
                 ("Padding_272_"   , ctypes.c_ubyte  * 6 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        self.header.StreamId.packet_type = 0
        self.header.StreamId.apid = 2
        self.header.StreamId.packet_version_number = 3


class ModelLinear (ctypes.Structure):
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


class ModelPolynomial (ctypes.Structure):
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


class ModelWaveform (ctypes.Structure):
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


class GPS_Cmd_M (ctypes.Structure):
    """/*!
* @brief GPS packet describing position info
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid GPS_Cmd_M_ID
*/
GPS_Cmd_M{
    /*!
    * @bigendian
    * @const StreamId.packet_type CCSDS_TLM
    * @const StreamId.apid GPS_Cmd_M_ID
    * @const StreamId.packet_version_number 3
    */
    CCSDS_PriHdr_t header;

    /*
    * @enum NOISE_MODELS
    */
    int noise_model;
    /*!
    * @depends noise_model LINEAR
    */
    ModelLinear linear;
    /*!
    * @depends noise_model POLYNOMIAL
    */
    ModelPolynomial poly;
    /*!
    * @depends noise_model WAVEFORM
    */
    ModelWaveform waveform;

"""
    _pack_ = 1
    _apid_ = 0
    _tlm_  = 1
    _fields_ = [ ("header"          , CCSDS_PriHdr_t     ),
                 ("Padding_48_64_"  , ctypes.c_ubyte * 2 ),
                 ("noise_model"     , ctypes.c_int32     ),
                 ("Padding_96_128_" , ctypes.c_ubyte * 4 ),
                 ("linear"          , ModelLinear        ),
                 ("poly"            , ModelPolynomial    ),
                 ("waveform"        , ModelWaveform      )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        self.header.StreamId.packet_type = 0
        self.header.StreamId.apid = 0
        self.header.StreamId.packet_version_number = 3


