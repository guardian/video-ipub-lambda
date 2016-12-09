#!/bin/bash

BUILDDIR=$PWD/deployable
mkdir -p video-ipub-lambda
mkdir -p ${BUILDDIR}
cp -r src/* ${BUILDDIR}
pip install -r requirements.txt -t ${BUILDDIR}

if [ ! -f /tmp/mysql-connector-python-2.1.4.tar.gz ]; then
    curl http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.1.4.tar.gz > /tmp/mysql-connector-python-2.1.4.tar.gz
fi
if [ ! -d /tmp/mysql-connector-python-2.1.4 ]; then
    cd /tmp; tar xvzf mysql-connector-python-2.1.4.tar.gz
fi
cd /tmp/mysql-connector-python-2.1.4; python ./setup.py install --home=${BUILDDIR} --install-lib ${BUILDDIR}

cd ${BUILDDIR}
zip -r ../video-ipub-lambda/video-ipub-lambda.zip *
cd ..

declare -x ARTEFACT_PATH=${BUILDDIR}/..
npm run deploy

if [ "$?" != "0" ]; then
    exit $? #propagate error for circleci
fi

rm -rf ${BUILDDIR}