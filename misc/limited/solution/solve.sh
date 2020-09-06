#!/bin/sh
tshark -r ../distfiles/packet.pcap -Tfields -e http.response_for.uri -e http.file_data -Y 'http.response and tcp.port == 8080' > flow.txt
