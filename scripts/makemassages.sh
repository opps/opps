#!/usr/bin/env bash
DIR=$(pwd)
for i in $(ls opps/)
do
	echo "make $i";
	mkdir -p $DIR/opps/$i/locale
	cd $DIR/opps/$i;
	django-admin.py makemessages -l en_US;
done

