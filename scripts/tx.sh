#!/usr/bin/env bash
DIR=$(pwd)
for i in $(ls opps/)
do
	echo "make $i";
	tx set --auto-local -r opps-core.$i "opps/$i/locale/<lang>/LC_MESSAGES/django.po" --source-language=en_US --source-file "opps/$i/locale/en_US/LC_MESSAGES/django.po" --execute;\
done

