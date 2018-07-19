# Simple redirect from HTTP to HTTPs

Useful to redirect Jenkins traffic from HTTP to HTTPs without Apache or Nginx.

On AWS EC2 you can use IPTables to redirect depending on root access port 80 to 8888 like this:

```
/sbin/iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80  -j REDIRECT --to-port 8888
/sbin/iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8443
```

