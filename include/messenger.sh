#/bin/bash
chat() {
  printf '%s: ' "$host_name"
  local message
  while [ 1 ]; do
    read -r message
    clear_line > $output
    printf '\033[0;36m%s: \033[0;39m%s\n%s: ' "$host_name" "$message" "$client_name" > $output
    move_cursor_up
    clear_line
    printf '\033[0;37m%s: \033[0;39m%s\n%s: ' "$host_name" "$message" "$host_name"
  done;
  echo chat ending
}