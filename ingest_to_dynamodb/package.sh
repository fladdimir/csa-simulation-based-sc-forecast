#!/bin/bash

echo "packaging..."

rm -rf function.zip
rm -rf package
mkdir package
pip install -r requirements.txt --target ./package
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py

echo "done."
