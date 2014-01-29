#!/bin/bash
DIR=$(pwd)
for i in $(ls opps/)
do
	if [[ -d $DIR/opps/$i ]]; then
		cd $DIR/opps/$i;
		# check if locale folder exists
		if [[ -e $DIR/opps/$i/locale/ ]]; then
			echo "make $i";
			django-admin.py compilemessages -v 3;
		fi
	fi
done

