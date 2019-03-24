#!/bin/env python
#coding:utf-8
#author:dxw
#function: build
#date:2016-07-13

import argparse
from string import Template
import os 
import sys

if len(sys.argv) < 7:
    eg = "eg: --projectName bbpayapi --projectNameDir BBPAYAPI_DIR --env production > build_bbpayapi.sh"
    print(eg)
    exit(1)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--projectName", action="store", dest="projectName")
parser.add_argument("--projectNameDir", action="store", dest="projectNameDir")
parser.add_argument("--env", action="store", dest="env")
result = parser.parse_args()

strsh='''
#!/bin/bash
#build_dxw_${projectName}.sh

PLATFORM_DIR=/home/dada/bebepayplatform
DEPLOY_DIR=$PLATFORM_DIR/deploy
BACK_DIR=$DEPLOY_DIR/back
WARS_DIR=$DEPLOY_DIR/wars

${projectNameDir}=$PLATFORM_DIR/${projectName}

svnNumber=$1

# cd $PLATFORM_DIR
cd $PLATFORM_DIR

# mkdir deploy/back
if [ -d deploy/back ];then
        echo "deploy and back isexist!"
else
        mkdir -p deploy/back
        echo "mkdir deploy/back ok!"
fi

# mkdir deploy/wars
if [ -d deploy/wars ];then
        echo "deploy and wars isexist!"
else
        mkdir -p deploy/wars
        echo "mkdir deploy/wars ok!"
fi

# cp deploy/files.war to back
cp $DEPLOY_DIR/${projectName}.war $BACK_DIR/${projectName}.war

# svn up
svn up

if [ $? -ne 0 ];then
        echo "platform svn up failed"
        exit 1
fi

cd $$${projectNameDir}
#svn up -r $1
svn up -r $svnNumber
if [ $? -ne 0 ];then
        echo "${projectName} svn up failed"
        exit 1
fi

# build
# mvn clean package -DskipTests -P ${env}
mvn clean package -DskipTests -P ${env}
if [ $? -ne 0 ];then
        echo "${projectName} build failed"
        exit 1
fi



#echo "cp $$${projectNameDir}/target/*.war $DEPLOY_DIR/${projectName}.war"
echo "cp $$${projectNameDir}/target/*.war $DEPLOY_DIR/${projectName}.war"

cp $$${projectNameDir}/target/*.war $WARS_DIR/${projectName}.war_$svnNumber
cp $$${projectNameDir}/target/*.war $DEPLOY_DIR/${projectName}.war
if [ $? -ne 0 ];then
        echo "cp ${projectName} failed"
        exit 1
fi

dt=`date`
echo "$dt &nbsp&nbsp&nbsp&nbsp $$${projectName} &nbsp&nbsp&nbsp&nbsp $$${projectNameDir} &nbsp&nbsp&nbsp&nbsp $svnNumber <br>" >> /usr/local/nginx/html/t.html

'''

d = dict(projectName=result.projectName, env=result.env, projectNameDir=result.projectNameDir)
#print("d: %s"%(d) )
print( Template(strsh).safe_substitute(d) )
