#/bin/bash
receive() {
  printf '%s: ' "$client_name" > $output
  declare -i message
  while IFS= read -r message; do
    clear_line
    printf '\033[0;36m%s: \033[0;39m%s\n%s: ' "$client_name" "$message" "$host_name"
    move_cursor_up > $output
    clear_line > $output
    printf '\033[0;37m%s: \033[0;39m%s\n%s: ' "$client_name" "$message" "$client_name" > $output
  done < $input
  echo receive ending
}
