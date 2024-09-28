#/bin/bash
host_name=host
client_name=client
port=9999
input=/tmp/chat-receive-$port
output=/tmp/chat-sending-$port

rm -f $input
rm -f $output
mkfifo $input 2>/dev/null
mkfifo $output 2>/dev/null

for i in ./include/*;
  do import $i 2>/dev/null
done

read -r -p 'Enter username: ' host_name
server &
echo 'Waiting for client to join...'
printf 'Enter username: ' > $output
read -r client_name < $input
echo "$client_name has joined the chat"
echo "Joined $host_name's chat" > $output
receive &
chat
