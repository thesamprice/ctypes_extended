#include "gps.h"

/* Define functions for each packet to process
* They take in a const void *, and return a status code
*/
int GPS_Cmd(const void *);
int Health(const void *);
int Pos(const void *);



int process_packet(const void * data){
    int status;
    /* Type cast input to a header type */
    const CCSDS_PriHdr_t * header = (const CCSDS_PriHdr_t*) data;
    /* get apid (Not proper way, but works for example)*/
    int apid = header->StreamId;

    switch(apid){
        case Health_M_ID:
            status = Health(data);
            break;
        case GPS_Cmd_M_ID:
            status = GPS_Cmd(data);
            break;;
        case Pos_M_ID:
            status = Pos(data);
            break;
        default:
            status = ERROR_UNKOWN_CMD; 
    }

    return status;
}

int GPS_Cmd(const void *data){
    const  GPS_Cmd_M * cmd =  (const GPS_Cmd_M *) data;
    int length = cmd->header.Length + 1 + 6;
    if(length != sizeof(cmd)){
        return ERROR_BAD_LENGTH;
    }
    return SUCCESS;
}
int Health(const void *data){
    const  Health_M * cmd =  (const Health_M *) data;
    int length = cmd->header.Length + 1 + 6;
    if(length != sizeof(cmd)){
        return ERROR_BAD_LENGTH;
    }


    return SUCCESS;
}
int Pos(const void *data){
    const Pos_M * cmd =  (const Pos_M *) data;
    int length = cmd->header.Length + 1 + 6;
    if(length != sizeof(cmd)){
        return ERROR_BAD_LENGTH;
    }

    return SUCCESS;
}