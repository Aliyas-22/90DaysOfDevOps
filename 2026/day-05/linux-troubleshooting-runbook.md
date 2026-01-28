## mini Runbook , using docker service ## 
## 1)-firstly we are going to check is available oeprating system is update or not we do = lsb_release -a
# output:
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.3 LTS
Release:        24.04
Codename:       noble
#
## 2)- done with checking install updates of ubuntu by doing this command = sudo apt update
## 3)- after updating install the softwere which is docker = sudo apt install docker.io
## 4)- to start docker service = sudo systemctl start docker 


## 5)- to see docker is started or not = sudo systemctl status docker
 # output:
 Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-01-28 09:12:07 UTC; 1min 35s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 2316 (dockerd)
      Tasks: 9
     Memory: 75.5M (peak: 75.8M)
#
   ## 6)- from running process give me the info about docker = ps aux|grep docker
# output
root        2316  0.0  7.4 1898084 69452 ?       Ssl  09:12   0:00 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ubuntu      2645  0.0  0.2   7076  2228 pts/0    S+   09:18   0:00 grep --color=auto docker
#

## 7)- to see the logs of recent process = journalctl -u docker
## output:
Jan 28 09:12:06 ip-172-31-47-83 systemd[1]: Starting docker.service - Docker Application Container Engine...
Jan 28 09:12:06 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:06.873194367Z" level=info msg="Starting up"
Jan 28 09:12:06 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:06.878404392Z" level=info msg="OTEL tracing is not configured, using no-op tracer provider"
Jan 28 09:12:06 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:06.881303833Z" level=info msg="detected 127.0.0.53 nameserver, assuming systemd-resolved, so usi>
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.022332342Z" level=info msg="Creating a containerd client" address=/run/containerd/containerd.>
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.141233917Z" level=info msg="Loading containers: start."
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.448804400Z" level=info msg="Loading containers: done."
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.479984532Z" level=info msg="Docker daemon" commit="28.2.2-0ubuntu1~24.04.1" containerd-snapsh>
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.480072424Z" level=info msg="Initializing buildkit"
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.493718413Z" level=warning msg="CDI setup error /etc/cdi: failed to monitor for changes: no su>
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.493746060Z" level=warning msg="CDI setup error /var/run/cdi: failed to monitor for changes: n>
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.523283046Z" level=info msg="Completed buildkit initialization"
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.531843038Z" level=info msg="Daemon has completed initialization"
Jan 28 09:12:07 ip-172-31-47-83 dockerd[2316]: time="2026-01-28T09:12:07.531889155Z" level=info msg="API listen on /run/docker.sock"
#
## 8)- to see the disk usage = df -h
# output:
Filesystem       Size  Used Avail Use% Mounted on
/dev/root         19G  2.3G   17G  13% /
tmpfs            458M     0  458M   0% /dev/shm
tmpfs            183M  904K  182M   1% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
efivarfs         128K  3.6K  120K   3% /sys/firmware/efi/efivars
/dev/nvme0n1p16  881M   89M  730M  11% /boot
/dev/nvme0n1p15  105M  6.2M   99M   6% /boot/efi
tmpfs             92M   12K   92M   1% /run/user/1000
Jan 28 09:12:07 ip-172-31-47-83 systemd[1]: Started docker.service - Docker Application Container Engine.
#
## 9)- to see the free ram available = free -h
# output:
               total        used        free      shared  buff/cache   available
Mem:           914Mi       393Mi       187Mi       2.7Mi       496Mi       520Mi
Swap:             0B          0B          0B
#
## 10)- to stop the service firstly we have to stop the scoket of docker then service we do = sudo systemctl stop docker.socket then sudo systemctl stop docker.service ##
