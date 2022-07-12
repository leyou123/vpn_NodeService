yum install lsof
yum -y install gcc gcc-c++ libffi-devel automake autoconf libtool make
yum -y install wget openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel libxml*
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar -xvf /root/Python-3.7.0.tgz
cd /root/Python-3.7.0
./configure --prefix=/usr/local/python3
make -j2
make install -j2
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
yum install python3-devel
pip3 install --upgrade pip
cd /root/vpn_NodeService
pip3 install -r requirements.txt