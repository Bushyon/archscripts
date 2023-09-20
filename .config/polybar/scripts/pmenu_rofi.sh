#!/bin/bash

# Program list
programs_name=$(pactl list sink-inputs | grep -Po 'media.name = "\K[^"]*')
programs_index=$(pactl list sink-inputs | grep -Po '(?<=Sink Input #).*')

# Sink list
sinks_name=$(pactl list sinks | grep -Po 'Description: \K.*')
sinks_index=$(pactl list sinks | grep -Po '(?<=Sink #).*')

# Format values and sizes
IFS=$'\n' p_n_db=($programs_name)
p_n_size=$((${#p_n_db[@]}+1))

IFS=$'\n' p_i_db=($programs_index)
p_i_count=${#p_i_db[@]}

IFS=$'\n' s_n_db=($sinks_name)
s_n_size=$((${#s_n_db[@]}+1))

IFS=$'\n' s_i_db=($sinks_index)
s_i_count=${#s_i_db[@]}

ret_prog=$(printf '%s\n' "${programs_name[@]}" | rofi -dmenu -lines $p_n_size)
# rofi will return an empty string if we haven't selected anything
# so let's return 0 instead
if [ -z "$ret_prog" ]; then
	exit 0
fi

ret_sink=$(printf '%s\n' "${sinks_name[@]}" | rofi -dmenu -lines $s_n_size)

if [ -z "$ret_sink" ]; then
	exit 0
fi

# Get indexes of ret_prog and ret_sink in *_name_db
for (( i = 0; i < ${#p_n_db[@]}; i++ )); do
	if [ "${p_n_db[$i]}" = "${ret_prog}" ]; then
		index_prog=$i;
	fi
done

for (( i = 0; i < ${#s_n_db[@]}; i++ )); do
	if [ "${s_n_db[$i]}" = "${ret_sink}" ]; then
		index_sink=$i;
	fi
done

# Execute command
ret=$(pactl move-sink-input ${p_i_db[$index_prog]} ${s_i_db[$index_sink]})

