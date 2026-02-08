# Day 15 – Networking Concepts: DNS, IP, Subnets & Ports
## Explain in 3–4 lines: what happens when you type google.com in a browser?
```
When we type google.com in a browser, the DNS server translates the domain name into an IP address.
The browser establishes a TCP connection with Google’s server.
Then it sends an HTTP/HTTPS request to fetch the webpage.
The server responds with data, and the page is displayed.
```
## What are these record types? Write one line each: A, AAAA, CNAME, MX, NS
```
A

google.com → 142.250.183.14

AAAA

google.com → 2404:6800:4007:81a::200e

CNAME

www.google.com
 → google.com
(alias → original)

MX

gmail.com → mail.gmail.com
(handles emails)

NS

google.com → ns1.google.com
(tells which DNS server manages domain)
```
## Run: dig google.com — identify the A record and TTL from the output
```
<img width="1920" height="336" alt="Screenshot (77)" src="https://github.com/user-attachments/assets/11ab99a6-c19e-4243-9aea-476a49359411" />
```
## What is an IPv4 address? How is it structured? (e.g., 192.168.1.10)
```
IPv4 (Internet Protocol version 4) is a 32-bit addressing system used to identify devices on a network.
It is divided into four 8-bit octets separated by dots, such as 192.168.1.10.
Each octet ranges from 0 to 255.
It supports about 4.3 billion unique IP addresses.
```
## Difference between public and private IPs — give one example of each
```
Public IP addresses are accessible over the internet and are globally unique, for example 8.8.8.8.
Private IP addresses are used inside local networks and are not directly accessible from the internet, for example 192.168.1.10.
```
## What are the private IP ranges?
```
These are private IP address ranges reserved for internal network communication. They are not accessible directly from the internet and are reused inside LANs. They help save public IP addresses using NAT.
```
## Run: ip addr show — identify which of your IPs are private
```
<img width="1920" height="589" alt="Screenshot (78)" src="https://github.com/user-attachments/assets/b29b2edb-7559-46e4-8c2c-838a7415312d" />

```
## What does /24 mean in 192.168.1.0/24?
## How many usable hosts in a /24? A /16? A /28?
## Explain in your own words: why do we subnet?
## Quick exercise — fill in:
## CIDR	Subnet Mask	Total IPs	Usable Hosts
## /24	? ?	?
## /16	?	?	?
## /28	?	?	?

```
 1) /24 = first 24 bits are network bits

IPv4 = 32 bits total
24 bits → network
8 bits  → host
```
```
2) /24

Host bits = 8
2⁸ = 256
256 − 2 = 254 usable hosts

 /16

Host bits = 16
2¹⁶ = 65,536
65,536 − 2 = 65,534 usable hosts

 /28

Host bits = 4
2⁴ = 16
16 − 2 = 14 usable hosts
```
```

3)3️⃣ Why do we subnet? 

Subnetting divides a large network into smaller networks to use IP addresses efficiently and improve network performance and security.
```
```
4) | CIDR | Subnet Mask     | Total IPs | Usable Hosts |
| ---- | --------------- | --------- | ------------ |
| /24  | 255.255.255.0   | 256       | 254          |
| /16  | 255.255.0.0     | 65,536    | 65,534       |
| /28  | 255.255.255.240 | 16        | 14           |
```
## What is a port? Why do we need them?
## Document these common ports:
## Port	Service
## 22	?
## 80	?
## 443	?
## 53	?
## 3306	?
## 6379	?
## 27017	?
## Run ss -tulpn — match at least 2 listening ports to their services
```
1) IP → finds the server

Port → finds the service inside the server
```
```
2) Because one computer runs many services at the same time.
```
```
3) | Port  | Service            |
| ----- | ------------------ |
| 22    | SSH (Secure Shell) |
| 80    | HTTP (Web)         |
| 443   | HTTPS (Secure Web) |
| 53    | DNS                |
| 3306  | MySQL              |
| 6379  | Redis              |
| 27017 | MongoDB            |
```


```
IP → finds the server

Port → finds the service inside the server
```
