#!/bin/sh
rm /home/ec2-user/delete_qualys_user.sh
sudo -i <<EOF2
/bin/cp -fp /etc/sudoers /etc/sudoers.qualys.bak
/bin/cp -fp /etc/passwd /etc/passwd.qualys.bak
/bin/cp -fp /etc/group /etc/group.qualys.bak
/bin/cp -fp /etc/shadow /etc/shadow.qualys.bak
useradd qualys
echo "qualys ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
su qualys <<EOF3
mkdir -p /home/qualys/.ssh
chmod 755 /home/qualys/.ssh
cd /home/qualys
curl -O -X GET -H "Content-Type:text/plain" https://ces-aws.cengage.info/services/dataservice/qualys/qualys_auth_scan/id_rsa.pub
cat ./id_rsa.pub > /home/qualys/.ssh/authorized_keys
chmod 600 /home/qualys/.ssh/authorized_keys
restorecon -R /home/qualys/.ssh
EOF3
EOF2
