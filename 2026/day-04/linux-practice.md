## systemd commands with output ##
1) sudo systemctl install nginx - this will basically install nginix in  our system. 
2) sudo systemctl start nginx - this will start the server nginx 
3) sudo systemctl status ssh - shows message which say :srvice open , service running on port 0.0.0.0.22 
4) sudo systemctl stop ngnix - stop the service
5) journalctl -u ngnix - to see the log it will show the services performance , or service is running reloading 
6) systemctl list-unites --type=service - by doing this you will see the description active running service details
7) ps - i sees the process which was done recently
8) top - live services list
9) pgrep nginx - basically we are telling to from all running services get the nginx service if available
10) tail -n 50 - to see the top 50 process 
