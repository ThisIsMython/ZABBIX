# ZABBIX监控系统资料
ztools是个人改进的zabbix数据获取脚本。
# SPEC文件和CentOS6一键安装包：
Name:zabbix-Cent-OS-6
Version:1.0.0
Release:1
Summary:zabbix install
Group:Monitor
License:GPL
Prefix:/usr/local
Source1:zabbix_agent
%description

%prep

%build

%install
echo "Copying files..."
mkdir -p %{buildroot}/usr/local/
cp -a %{SOURCE1} %{buildroot}/usr/local/

%files
/usr/local/zabbix_agent/

%pre
echo "Creating user zabbix and group zabbix."
groupadd zabbix
useradd -g zabbix zabbix
echo zabbix:zabbix | chpasswd
sed -i '/^root/a\zabbix	ALL=(ALL)	NOPASSWD: ALL' /etc/sudoers

echo "zabbix/zabbix created successfully!"

%post
echo "Configuring zabbix..."
chown -R zabbix:zabbix /usr/local/zabbix_agent/
chmod -R 755 /usr/local/zabbix_agent/
echo "zabbix installed successfully!"
echo  ""
echo "Starts and stops Zabbix Agent using chkconfig"
cp /usr/local/zabbix_agent/etc/zabbix_agentd /etc/init.d/
chkconfig --add zabbix_agentd
chkconfig --level 345 zabbix_agentd on
chkconfig --list|grep zabbix
echo  ""
echo "Starting zabbix_agentd"
su - zabbix
/usr/local/zabbix_agent/sbin/zabbix_agentd -c /usr/local/zabbix_agent/etc/zabbix_agentd.conf
echo ""
echo "Chenck zabbix agent PORT 10050:"
netstat -tuln|grep 10050|echo >1
echo  ""
echo "###############CHECK ZABBIX_AGENT PROCESSES###################"
ps -ef|grep zabbix

%preun

%postun
killall zabbix_agentd
userdel -r zabbix
sed -i "/^zabbix/d" /etc/sudoers
rm -rf /etc/init.d/zabbix_agentd
echo "zabbix uninstalled successfully!"


# 打包之后zabbix监控客户端安装包：
zabbixzabbix-Cent-OS-6-1.0.0-1.i686.rpm
