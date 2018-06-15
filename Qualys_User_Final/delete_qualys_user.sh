#!/bin/sh
rm /home/ec2-user/qualys.sh*
sudo -i << EOF1
userdel qualys
rm -rf /home/qualys
rm -rf /var/spool/mail/qualys
#sed -i "s/test\sALL=(ALL)\sNOPASSWD:\sALL//g" /etc/sudoers
/bin/cp -fp /etc/sudoers.qualys.bak /etc/sudoers
EOF1
