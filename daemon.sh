#!/bin/bash

case "$1" in
  start)
    echo "Starting server"
    # Start the daemon 
    python3 /home/alex/git/image_to_hearts/bot.py start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python3 /home/alex/git/image_to_hearts/bot.py  stop
    ;;
  restart)
    echo "Restarting server"
    python3 /home/alex/git/image_to_hearts/bot.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "daemon.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0

