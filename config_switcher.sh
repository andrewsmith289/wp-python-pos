#!/bin/bash
FILE="/home/pi/possystem/.conf/hdmi/CONF_SWAP"
DIR=$(dirname "${FILE}")

START="# {{bcb_pos}}"
END="# {{end_bcb_pos}}"

TARGET_CONF="/boot/config.txt"

if [ ! -d "$DIR" ];
then
    mkdir -p "$DIR"
fi

if [ -f "$FILE" ];
then
   rm "${FILE}"
   sudo sed -i "/${START}/,/${END}/d" "${TARGET_CONF}"
else
   touch "${FILE}"

   if ! grep -q "${START}" "$FILE";
   then
       read -r -d '' CONF_FRAGMENT << EOM

# {{bcb_pos}}
hdmi_force_hotplug=0
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
max_usb_current=1
# {{end_bcb_pos}}
EOM
        sudo echo "${CONF_FRAGMENT}" >> ${TARGET_CONF}
   fi
fi
