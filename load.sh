#!/bin/bash

# mkdir -p ./data/
# ssh test-stand 'tar zcvf /tmp/csvs.tar.gz /root/csvs/*'
# scp test-stand:/tmp/csvs.tar.gz ./data/
# ssh test-stand 'rm /tmp/csvs.tar.gz'
# tar zxvf ./data/csvs.tar.gz -C ./data/
# mv ./data/root/csvs/* ./data/

ls ./data/*.csv | xargs cat > ./ttt

sed -i '/WPA/d;/BSSID/d;/, , ,/d;/^\s*$/d' ./ttt
