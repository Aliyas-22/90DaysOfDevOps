# Day 14 – Networking Fundamentals & Hands-on Checks
### 7 LAYERS OF OSI MODEL:- 
# OSI MODEL EXPLAIN HOW DATA MOVES STEP-BY-STEP THROUGH 7 LAYERS FROM APPLICATION TO PHYSICAL NETWORK
1)Application:- user application ex: browser , whatsapp


2)presentation layer :- encryption & formatting ex:HTTPS , SSL


3)session layer:- START/END connection ex:login session


4)transport layer: Reliable delivery ex:tcp/udp, ports


5)network layer:-IP & routing ex:IP address and router


6)data-link layer:mac address ex:switch


7)physical layer: Hardwere ex: cable ,wi-fi

# TCP/IP MODEL VS OSI MODEL: Both osi model and tcp/ip models explain how data travels between device in a network
## OSI is theoretical model used for learning and 
## TCP/IP is a practical model used in the real internet

### OSI → 7 Layers
1. Application
2. Presentation
3. Session
4. Transport
5. Network
6. Data Link
7. Physical

### TCP/IP → 4 Layers
1. Application
2. Transport
3. Internet
4. Network Access

---

## Layer Mapping

| OSI Layers | TCP/IP Layer |
|------------|--------------|
| Application + Presentation + Session | Application |
| Transport | Transport |
| Network | Internet |
| Data Link + Physical | Network Access |

---

## Key Differences

| Feature | OSI | TCP/IP |
|-----------|-----------|-----------|
| Type | Theoretical | Practical |
| Layers | 7 | 4 |
| Used in real internet | No | Yes |
| Complexity | More | Simple |
| Purpose | Learning & understanding | Real communication |

---

## Example (Sending WhatsApp Message)

OSI:
App → Present → Session → Transport → Network → Data link → Physical

TCP/IP:
Application → Transport → Internet → Network Access

Both do same work, but TCP/IP combines layers.

---

## Why TCP/IP is important for DevOps?

In real DevOps work we use:

- HTTP/HTTPS → Application
- TCP/UDP & Ports → Transport
- IP, VPC, Routing → Internet
- Cables/WiFi → Network Access

So TCP/IP is what actually runs AWS, servers, and the internet.

---

## One-line Interview Answer

OSI is a 7-layer theoretical model for understanding networking, while TCP/IP is a 4-layer practical model used for real-world internet communication.

# Where protocols sit in TCP/IP stack

Application → HTTP, HTTPS, DNS
Transport → TCP, UDP
Internet → IP
Network Access → Ethernet/WiFi

Example:
curl https://example.com
= HTTPS over TCP over IP

