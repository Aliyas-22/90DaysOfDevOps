# 🚀 Day 8 – Deploying Nginx Web Server on AWS EC2

## 📌 Objective
Deploy a real web server on the cloud and learn practical server management using AWS EC2 and Linux.

---

## 🛠️ Tasks Performed
- Launched AWS EC2 instance  
- Connected via SSH  
- Installed and configured Nginx  
- Opened HTTP port 80 in Security Group  
- Collected server logs  
- Transferred logs to local machine using SCP  
- Verified web server is accessible from the internet  

---

## 🔐 Step 1 – Connect to EC2

```bash
chmod 400 key.pem
ssh -i key.pem ubuntu@<public-ip>
```

---

## 🔄 Step 2 – Update Packages

```bash
sudo apt update
```

---

## 📦 Step 3 – Install Nginx

```bash
sudo apt install nginx -y
```

---

## ▶️ Step 4 – Start & Enable Nginx

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

---

## 🌐 Step 5 – Configure Security Group

Allow inbound rule:

- Type: HTTP  
- Port: 80  
- Source: 0.0.0.0/0  

---

## ✅ Step 6 – Verify Web Server

Open in browser:

```
http://http://13.60.196.193/
```

Nginx default page should load successfully.

---

## 📜 Step 7 – Check & Save Logs

```bash
journalctl -u nginx
journalctl -u nginx | tee nginxlogs.txt
```

---

## 📥 Step 8 – Transfer Logs to Local Machine

Exit server:

```bash
exit
```

Run from local terminal:

```bash
scp -i key.pem ubuntu@<public-ip>:/home/ubuntu/nginxlogs.txt .
```

---

## Outcome
✅ Successfully deployed cloud-based web server  
✅ Hosted live Nginx webpage  
✅ Practiced SSH & SCP  
✅ Learned log management  
✅ Improved troubleshooting skills  

---
## screenshots 
<img width="1920" height="1080" alt="Screenshot (32)" src="https://github.com/user-attachments/assets/919568a3-d0ae-4e3f-940f-c72811e42aa1" />
<img width="1920" height="1080" alt="Screenshot (30)" src="https://github.com/user-attachments/assets/851f436e-24a3-4cdd-9e14-ba0277f52d80" />

<img width="1920" height="1080" alt="Screenshot (35)" src="https://github.com/user-attachments/assets/ad776a97-ffd8-4b65-afbe-31757bdf35bd" />
