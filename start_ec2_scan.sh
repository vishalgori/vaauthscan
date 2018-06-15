#!/bin/sh
#Generate RSA key pair
mkdir ./.ssh
chmod 700 ./.ssh
ssh-keygen -t rsa -f ./.ssh/id_rsa -N ''

#Copying over public key to CES to be retreived by hosts
curl -H "Content-Type:text/plain" -X "POST" -d @id_rsa.pub https://ces-aws..info/services/dataservice/qualys/qualys_auth_scan/id_rsa.pub

#Copy private key into a variable to be used later below
key="$(<./.ssh/id_rsa)"

#Copying list of IPs to be considered for auth scan to be used later below
#ips=`cat EC2-QA`
ips=`cat IAS-DEV-test | tr -dc '[:digit:],."[]'`

#Create Authentication record in Qualys
#curl -H "X-Requested-With: Curl" -u "user:password" -X "POST" -d "action=create&echo_request=1&title=EC2boxQualysAuth&ips=$ips&username=qualys" --data-urlencode "rsa_private_key=$key" "https://qualysapi.qualys.com/api/2.0/fo/auth/unix/"

#Create a Tag to be used to select our Host IPRange
curl -u "user:pass" -H "Content-type: text/xml" -X "POST" --data-binary @- "https://qualysapi.qualys.com/qps/rest/2.0/create/am/tag" < ./file.xml.bak -o ./New_Tag_EC2_box

#Updating existing Authentication record created before.
Auth_RecID=`grep "</ID>" ./Existing_Auth_Record_EC2_box |egrep -o [0-9]+`
curl -H "X-Requested-With: Curl" -u "user:pass" -X "POST" -d "action=update&ids=$Auth_RecID&echo_request=1&ips=$ips&username=qualys" --data-urlencode "rsa_private_key=$key" "https://qualysapi.qualys.com/api/2.0/fo/auth/unix/" -o ./New_Auth_Record_EC2_box_update

#Evaluate all tags
curl -u "user:pass" -H "content-type:text/xml" -X POST --data-binary @evaluate.xml "https://qualysapi.qualys.com/qps/rest/2.0/evaluate/am/tag"

#Obtaining newly created Tag's ID
TagID=`grep id ./New_Tag_EC2_box |egrep -o [0-9]+`

#Initiate IAS-scan
sleep 60

#Initiate EC2-scan
curl -H "X-Requested-With: Curl" -u "user:pass" -X "POST" -d "action=launch&scan_title=EC2boxQAAuthScan&connector_name=ec2-Connector-AWS-QA&ec2_endpoint=us-east-1&target_from=tags&use_ip_nt_range_tags=0&tag_include_selector=any&tag_set_by=id&tag_set_include=$TagID&option_id="282448"&iscanner_name=AWS-QA" "https://qualysapi.qualys.com/api/2.0/fo/scan/" > outputfile.txt

#API call to qualys to check when scan is done
curl -H 'X-Requested-With: Curl Sample' -u "user:pass" 'https://qualysapi.qualys.com/api/2.0/fo/scan/?action=list&scan_ref=scan/1458568835.89586&echo_request=1&show_status=1'
