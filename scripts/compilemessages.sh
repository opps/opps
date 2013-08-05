#!/usr/bin/env bash
DIR=$(pwd)
for i in $(ls opps/)
do
	echo "make $i";
	cd $DIR/opps/$i;
	django-admin.py compilemessages;
done

