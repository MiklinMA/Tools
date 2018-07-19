#!/usr/bin/env bash
# 
# 2018
# Mike Miklin <MiklinMA@gmail.com>
#
# Give an access for any inbound traffic 
# on service group for public IP of local machine
# 

inst="i-0f4bacddf2d743c6f"

start() {
    echo "Start $inst" >&2
    aws ec2 start-instances \
        --instance-ids $inst \
        --output text
}

stop() {
    echo "Stop $inst" >&2
    aws ec2 stop-instances \
        --instance-ids $inst \
        --output text
}

status() {
    echo "Status $1" >&2

    res=$(aws ec2 describe-instances \
        --instance-ids $inst \
        --output text)

    if [ -z "$1" ]; then
        echo "$res" | grep "STATE\s\|TAGS\sName"

    elif [ "$1" == "ip" ]; then
        echo "$res" \
            | grep -A1 "NETWORKINTERFACES\s" \
            | grep "ASSOCIATION\s" \
            | awk '{print $4}'

    else
        echo "$res"
    fi
}

case $1 in
    "start")
        start
        ;;
    "stop")
        stop
        ;;
    "status")
        status full
        ;;
    "ip")
        status ip
        ;;
    *)
        status
        ;;
esac
