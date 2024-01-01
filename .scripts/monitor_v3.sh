W_MM=$((698/2))
H_MM=$((393/2))

W_PX=1920
H_PX=1080

do_the_thing() {
  xrandr --delmonitor LEFT || true
  xrandr --delmonitor RIGHT || true
  xrandr --delmonitor TOP || true
  xrandr --delmonitor BOTTOM || true

  xrandr --setmonitor LEFT \
    ${W_PX}/${W_MM}x${H_PX}/${H_MM}+0+0 $LEFT_OUTPUT
  xrandr --setmonitor RIGHT \
    ${W_PX}/${W_MM}x${H_PX}/${H_MM}+${W_PX}+0 $RIGHT_OUTPUT
  xrandr --setmonitor TOP \
    ${W_PX}/${W_MM}x${H_PX}/${H_MM}+0+$H_PX $TOP_OUTPUT
  xrandr --setmonitor BOTTOM \
    ${W_PX}/${W_MM}x${H_PX}/${H_MM}+${W_PX}+$H_PX $BOTTOM_OUTPUT
}

move_workspace() {
  WORKSPACE=$1
  OUTPUT=$2
  echo "Moving workspace $WORKSPACE to output $OUTPUT."
  i3-msg "workspace $WORKSPACE; move workspace to output $OUTPUT"
}

# Let's check if there is a 4K monitor.
OUTPUT=$(xrandr -q | grep 3840x2160 | cut -d" " -f1)
if [ "$OUTPUT" ]; then
  echo "Detected 4K monitor (output=$OUTPUT)."
  LEFT_OUTPUT=none
  RIGHT_OUTPUT=none
  TOP_OUTPUT=none
  BOTTOM_OUTPUT=none
  do_the_thing

  #i3-msg "workspace 1; move workspace to output RIGHT"
  #i3-msg "workspace 2; move workspace to output LEFT"
  i3-msg "workspace 3; move workspace to output TOP"
  i3-msg "workspace 4; move workspace to output BOTTOM"

  exit 0
fi

# Add additional checks for other monitor configurations as needed.

echo "Could not find any recognized monitor arrangement. Sorry."

