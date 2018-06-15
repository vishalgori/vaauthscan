#!/bin/sh
#scan_ref=`grep -i "scan/" ./IAS-scan |egrep -o "[0-9]+.[0-9]+"`
scan_ref=`grep -i "scan/" ./IAS-scan |egrep -o "scan/([0-9]+)\.([0-9]+)"`
curl -H "X-Requested-With: Curl" -u "user:password" -X "POST" -d "action=fetch&scan_ref=$scan_ref" "https://qualysapi.qualys.com/api/2.0/fo/scan/"
