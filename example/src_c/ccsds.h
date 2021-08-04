
#ifndef  __CCSDS_H_
#define  __CCSDS_H_

#include <stdint.h>

enum CCSDS_CMD_TLM{
    CCSDS_TLM=0,
    CCSDS_CMD=1
};

enum TRUE_FALSE{
    TF_FALSE=0,
    TF_TRUE=1,
};

/*!
* @bigendian
*/
typedef struct __attribute__ ((packed))  CCSDS_PriHdr_t{
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
} __attribute__ ((packed)) CCSDS_PriHdr_t;

#endif // ! __CCSDS_H
