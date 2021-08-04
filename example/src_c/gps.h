#ifndef GPS_H
#define GPS_H
#include "ccsds.h"

enum app_apids{
    GPS_Cmd_M_ID=0,
    Health_M_ID=1,
    Pos_M_ID=2,


};

/*!
* @brief Packet health
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid Health_M_ID
*/
typedef struct Health_M{
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

}Health_M;

enum CordFrame{
    ECEF=1,
    J2K=2,
    LATLONG=3
};

/*!
* @brief GPS packet describing position info
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid Pos_M_ID
*/
typedef struct Pos_M{
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

}Pos_M;

enum NOISE_MODELS{
    LINEAR,
    POLYNOMIAL,
    WAVEFORM
};

/*!
* @brief describes y=x*slope + const
*/
typedef struct ModelLinear
{
    /*!
    * @brief constant
    */
    double cons;
    /*!
    * @brief slope
    */
    double slope;
}ModelLinear;

/*!
* @brief describes y=x_0 + x_1*x + x_2*x*x
*/
typedef struct ModelPolynomial
{
    double x_0;
    double x_1;
    double x_2;

}ModelPolynomial;

/*!
* @brief describes y=a*sin(x) + b*cos(x)
*/
typedef struct ModelWaveform
{
    double a;
    double b;

}ModelWaveform;

/*!
* @brief GPS packet describing position info
* @ingroup MESSAGES
* @ID_ITEM header.StreamId.apid GPS_Cmd_M_ID
*/
typedef struct GPS_Cmd_M{
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

}GPS_Cmd_M;


#endif