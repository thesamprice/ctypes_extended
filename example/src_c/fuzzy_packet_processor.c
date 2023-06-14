
#include "gps.h"
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
extern int process_packet(const void * data);

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Type cast input to a header type */
    const CCSDS_PriHdr_t * header = (const CCSDS_PriHdr_t*) data;

    /* Throw out any test data that does not have a proper length 
    * We dont want fuzzer to generate a bunch of bad length packets, we can do that manually.
    * CCSDS Length attribute is size of payload -1, header is 6 bytes.
    */
    int payload_size = header->Length +1;
    int length = payload_size + 6 ;
    if(length != size){
        return -1;
    }

    /* Do something interesting */
    process_packet(data);

    return 0;  // Values other than 0 and -1 are reserved for future use.
}