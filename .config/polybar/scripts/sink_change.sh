#!/bin/bash

# Rotates between sink devices (sound output devices).
rotate_sound_cards() {
    active_sink=$(pactl get-default-sink)
    sinks=$(pactl list short sinks | grep -v "hdmi" | awk '{print $2}')
    
    if [[ -z $active_sink || -z $sinks ]]; then
        echo "Unable to retrieve sound cards or HDMI sinks"
        exit 1
    fi
    for sink in $sinks; do
        if [[ $sink != $active_sink ]]; then
            pactl set-default-sink "$sink"
            echo "Rotated sound card: $active_sink to $sink"
            break
        fi
    done
}

# This is a customized part, change the strings as you need. 
device(){
    active_device=$(pactl get-default-sink)
    volume=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -Po '\d+(?=%)' | head -n 1)

    if [[ $active_device == *"Focusrite"* ]]; then
        echo "$volume - 🎧"
    elif [[ $active_device == *"pci"* ]]; then 
        echo "$volume - 🔈"
    else 
        echo Not Configured
    fi
}

if [ $1 = "--change" ]; then
    rotate_sound_cards
elif [ $1 = "--device" ]; then
    device
fi
