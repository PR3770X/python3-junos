PID=$(top -b | grep bbe-smgd | awk '{print $1}') && [ -n "$PID" ] && kill -9 $PID
