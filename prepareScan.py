import time, requests, credstash, os
import hashlib, datetime
import logging, json

def lambda_handler(event,context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #logger.info('got event{}'.json.dumps(event))
    #logger.error('something went wrong')
    sns_message=json.loads(event['Records'][0]['Sns']['Message'])
    logger.info('SNS message received: '+str(sns_message))

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True




    timeStamp = time.time()
    requestTimestamp = datetime.datetime.fromtimestamp(int(timeStamp)).strftime('%Y-%m-%d %H:%M:%S')
    endPoint = os.environ['endPoint']       #IAS/qualys/prepareScan
    #url = "https://ias.cengage.info/IAS/qualys/prepareScan"
    url = os.environ['url']
    #accessKey=os.environ['accessKey']
    #secretKey=os.environ['secretKey']
    accessKey = credstash.getSecret("IAS-accessKey")
    secretKey = credstash.getSecret("IAS-secretKey")
    #payload = json.load(open("test"))
    #data = json.dumps(sns_message['PrivateIP'])
    data = ["10.172.104.117", "10.172.105.202", "10.172.253.71"]
    stringToHash = endPoint + accessKey + requestTimestamp + secretKey
    calculatedSignatureHash = hashlib.sha1(stringToHash).hexdigest()
    print calculatedSignatureHash
    #calculatedSignatureHash = DigestUtils().getHexSha1Digest(stringToHash)
    headers = {'content-type': 'application/json', 'accessKey' : str(accessKey), 'secretKey' : str(secretKey) ,'requestSignature' : calculatedSignatureHash, 'requestTimestamp' : str(requestTimestamp) , 'requestEndpoint' : str(endPoint)}
    response=requests.post(url, data=data, headers=headers)
    logger.info("AppBuilder requested to prepare requested list of IPs for scanning: "+str(response))
