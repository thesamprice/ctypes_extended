```bash
cd src_c
# Compile packet processor example as a shared library
# windows dll, linux .so, mac dylib
# include fuzzy, and address sanitizing

clang -g -O1 -fsanitize=fuzzer,address --shared packet_processor.c -o packet_processor.dylib 
# compile fuzzy tester
clang -Wno-nullability-completeness -g -O1 -fsanitize=fuzzer,address fuzzy_packet_processor.c -o fuzzy_packets
```