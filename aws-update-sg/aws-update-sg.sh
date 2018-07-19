#!/usr/bin/env bash
# 
# 2018
# Mike Miklin <MiklinMA@gmail.com>
#
# Give an access for any inbound traffic 
# on service group for public IP of local machine
# 

sg="sg-0583db12dd5a74ddd"
ip=$(curl -s ipinfo.io/ip 2>/dev/null)

if [ -z "$ip" ]; then
    echo "No public IP found."
    exit 1
fi

aws ec2 describe-security-groups \
    --group-ids $sg --output text \
    2>/dev/null \
    | grep "IPPERMISSIONS\s" -A1 \
    | grep IPRANGES

if [ $? -eq 0 ]; then
    aws ec2 authorize-security-group-ingress \
        --group-id $sg --protocol all --cidr $ip/32 \
        > /dev/null 2>&1 \
        && echo $ip got access to $sg \
        || echo $ip already have an access to $sg
else
    echo $sg not found
fi

