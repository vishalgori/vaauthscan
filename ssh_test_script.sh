#!/bin/bash
while read HOST ; do ssh -o "StrictHostKeyChecking no" -o "ConnectTimeout=3" -o "PasswordAuthentication no" qualys@$HOST -i ./.ssh/id_rsa "uname -a" < /dev/null; echo $HOST; done < test >&testremaining
