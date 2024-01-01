undo_the_thing() {
  xrandr --delmonitor LEFT || true
  xrandr --delmonitor RIGHT || true
  xrandr --delmonitor TOP || true
  xrandr --delmonitor BOTTOM || true

  # Set the primary screen (adjust if necessary)
  xrandr --output PRIMARY --primary
}
undo_the_thing
