#!/bin/sh

#Obtaining corresponding scan reference number
REF=`grep -i value ./IAS-scan |egrep -o "scan/[0-9]+.[0-9]+"`


#API call to qualys to check when scan is done
curl -H "X-Requested-With: Curl" -u "user:pass" --data-urlencode "action=list" --data "scan_ref=$REF&echo_request=1&show_status=1" "https://qualysapi.qualys.com/api/2.0/fo/scan/" -o ./scan_status

#Grep for scan status. If completed delete qualys user.
ips=`cat IAS-DEV | tr -dc '[:digit:],."[]'`
curl -v -H "Content-Type:application/json" -X "POST" -d "$ips" "https://ias.cengage.info/IAS/qualys/cleanupScan" --trace-ascii /dev/stdout
