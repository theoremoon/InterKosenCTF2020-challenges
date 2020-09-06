#!/bin/bash
if [[ "$FLAG" =~ ^KosenCTF\{[-a-zA-Z0-9_!?]+\}$ ]]; then
    echo $FLAG | ./chall > flag.enc
else
    echo "Invalid flag"
fi
