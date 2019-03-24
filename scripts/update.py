#!/bin/env python
#coding:utf-8
#author:dxw
#function: update
#date:2016-07-13

import argparse
from string import Template
import os 
import sys

if len(sys.argv) < 9:
    eg = "eg: --projectName ebomp --projectTomcatDir TOMCAT_EBOMP_DIR --user bebepay --userDir run_pkgs > update_bbpayapi.sh"
    print(eg)
    exit(1)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--projectName", action="store", dest="projectName")
parser.add_argument("--projectTomcatDir", action="store", dest="projectTomcatDir")
parser.add_argument("--user", action="store", dest="user")
parser.add_argument("--userDir", action="store", dest="userDir")
result = parser.parse_args()

strsh='''
#!/bin/bash
#
#update_dxw_${projectName}.sh

#set Shell Variable
RUN_DIR=/home/${user}/${userDir}

${projectTomcatDir}=/usr/local/tomcat-${projectName}

#stop tomcat-${projectName}
tomcat_${projectName}_pid=`ps -ef |grep java |grep tomcat-${projectName} |grep -v grep |awk '{print $2}' `

echo "start kill tomcat-${projectName} ..."
sudo kill -9 $tomcat_${projectName}_pid
if [ $? -ne 0 ];then
    echo "stop tomcat-${projectName} faill!!"
fi

#rm ${projectName}
echo "rm ${projectName} from tomcat-${projectName}..."
sudo rm -rf $$${projectTomcatDir}/webapps/${projectName}*
if [ $? -ne 0 ];then
    echo "rm ${projectName} on tomcat-${projectName} faill!!"
fi

#cp ${projectName}.war
echo "cp ${projectName}.war to tomcat-${projectName} ..."
sudo cp $RUN_DIR/${projectName}.war $$${projectTomcatDir}/webapps/${projectName}.war
if [ $? -ne 0 ];then
    echo "cp ${projectName}.war to tomcat-${projectName} faill!!"
    exit 1
fi

#start tomcat-${projectName}
echo "start tomcat-${projectName} ..."
sudo $$${projectTomcatDir}/bin/startup.sh
if [ $? -ne 0 ];then
    echo "start tomcat-${projectName} faill!!"
    exit 1
else
    echo "start tomcat-${projectName} ok!!"
fi


'''


d = dict(user=result.user, userDir=result.userDir, projectName=result.projectName, projectTomcatDir=result.projectTomcatDir)
s = Template(strsh).safe_substitute(d)
print(s)
