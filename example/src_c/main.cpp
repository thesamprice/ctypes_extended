#include <string>
#include <filesystem>
namespace fs = std::filesystem;
extern const char *TESTDATAPATH;




TEST(bool DISABLED_GeonsFuzzer,std::string FuzzerFiles)
{
    std::string folder_path = TESTDATAPATH;
    folder_path = folder_path + "/fuzzer/copus";
    const size_t header_size = sizeof(GeonsCFE_SB_CmdHdr_t);
    DIR* directory = opendir(folder_path.c_str());
    uint8_t buffer[1024*24];
    if (directory) {
        struct dirent* entry;
        while ((entry = readdir(directory)) != nullptr) {
            if (entry->d_type == DT_REG) { // Regular file
                /* std::cout << entry->d_name << std::endl; */
                std::string filename = folder_path + "/" + entry->d_name;
                FILE * fid = fopen(filename.c_str(),"rb");

                size_t num_read = fread(buffer, 1 , header_size, fid);
                if(num_read != header_size){
                    std::cout << "Failed to read header for : " << entry->d_name << std::endl;
                    fclose(fid);
                    continue;
                }

                size_t payload_size = GeonsCCSDSGetLength((GeonsCFE_SB_CmdHdr_t*)buffer) - header_size;
                if((payload_size + header_size) > sizeof(buffer)){
                    FAIL() << "buffer size needs increased to " << payload_size + header_size << std::endl;
                    fclose(fid);
                    continue;
                }

                num_read = fread( &buffer[header_size],1,payload_size, fid );
                if(num_read != payload_size){
                    std::cout << "Failed to payload for : " << entry->d_name << "got " << num_read << " wanted " << payload_size << std::endl;
                    fclose(fid);
                    continue;
                }
                LLVMFuzzerTestOneInput(buffer,header_size + payload_size);

                fclose(fid);
            }
        }
        closedir(directory);
    } else {
        FAIL() << "Error: Unable to open directory: " << folder_path << std::endl;
    }

}

int main()
{
    fs::create_directories("./testFolder");
    TEST(true, "./testFolder");
}