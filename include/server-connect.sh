#/bin/bash
allocate(){
  echo "echo \"ncat is listening\"" > ncat
  chmod +x ncat 2>/dev/null
  export PATH=$(pwd):$PATH
}

deallocate(){
  export PATH=${PATH%:$(pwd)}
  rm -f $(pwd)/ncat 2>/dev/null
}

server() {
  allocate
  echo "Starting on port $port"
  ncat -l -p $port > $input &
  echo "server ending"
  deallocate
}