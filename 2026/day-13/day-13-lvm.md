# Day 13 – Linux Volume Management (LVM)
## steps to follow for creating pysical volume 
```
1) create a 3 volume in your instance
2) lsblk (use to see list of attached volume and disk )
3) sudo su (run as a root always)
4) lvm
5) pvs
6)pv create /dev/xvdf /dev/xvdg /dev/xvdg
7) pvs
```
## steps to create volume group
```
1)vgcreate devops-vg /dev/xvdf /dev/xvdg
2) vgs
```
## steps to create logical volume
```
1)lvcreate -l 10G -n devops-lv devops-vg
2)lvs
3)lvdisplay
```
## steps to mount the volume
```
1)lvs
2)mkdir /mnt/devops_lv_mount
3)mkfs .ext4 /dev/devops-vg/devops-lv
4) mount /dev/devops-vg/devops-lv /mnt/devops_lv_mount
5) df -h
6) cd /mnt/devops_lv_mount/
7) mkdir learn
8) ls ,cd learn/ , vim devops_learn.txt ,echo "hello learner" , cd .. , cat /mnt/devops_lv_mount/learn/devops_learn.txt
```
## extend the logical volume
```
df -h
lvm
lvextend -l -5 /dev/devops_vg/devops-lv
df -h
lsblk
```
