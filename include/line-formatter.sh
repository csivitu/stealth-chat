#/bin/bash
clear_line() {
  printf '\r[2K'
}

move_cursor_up() {
  printf '[1A'
}
