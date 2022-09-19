#!/bin/bash

secret=$(aws ssm get-parameter --name "$1" --region "$2" --with-decryption --query "Parameter.Value" --output text)

yum update -y
amazon-linux-extras install mate-desktop1.x
echo 'PREFERRED=/usr/bin/mate-session' > /etc/sysconfig/desktop
yum -y install tigervnc-server
yum -y install expect

echo '#!/bin/sh' > /home/ec2-user/script.sh
echo 'prog=/usr/bin/vncpasswd' >> /home/ec2-user/script.sh
echo 'mypass="newpass"' >> /home/ec2-user/script.sh
echo '/usr/bin/expect <<EOF' >> /home/ec2-user/script.sh
echo 'spawn "$prog"' >> /home/ec2-user/script.sh
echo 'expect "Password:"' >> /home/ec2-user/script.sh
echo 'send '"$secret\r"'' >> /home/ec2-user/script.sh
echo 'expect "Verify:"' >> /home/ec2-user/script.sh
echo 'send '"$secret\r"'' >> /home/ec2-user/script.sh
echo 'expect "Would*"' >> /home/ec2-user/script.sh
echo 'send "n\r"' >> /home/ec2-user/script.sh
echo 'expect eof' >> /home/ec2-user/script.sh
echo 'exit' >> /home/ec2-user/script.sh
echo 'EOF' >> /home/ec2-user/script.sh

chmod 777 /home/ec2-user/script.sh
su -c '/home/ec2-user/script.sh' ec2-user

mkdir /etc/tigervnc
echo '#localhost' > /etc/tigervnc/vncserver-config-mandatory
cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@.service
sed -i 's/<USER>/ec2-user/' /etc/systemd/system/vncserver@.service
systemctl daemon-reload
systemctl enable vncserver@:1
systemctl start vncserver@:1

wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
yum -y install ./google-chrome-stable_current_*.rpm

rm /home/ec2-user/script.sh
rm /home/ec2-user/linux-user-data.sh
