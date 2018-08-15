CLOUDFLARE_EMAIL    = ""                # ENTER EMAIL ADDRESS
CLOUDFLARE_API      = ""                # ENTER API KEY

CLOUDFLARE_SITES    = [{
        'zone_id':      "",             # ENTER ZONE ID
        'name':         "",             # ENTER NAME
        'dns_id':       ""              # ENTER DNS ID
}]										# ADD NEW DICT OBJECTS TO THE LIST FOR MORE THAN ONE TYPE

###############################################################################################################################
CLOUDFLARE_ENDPOINT  = "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_ID}"
CLOUDFLARE_HEADER    = {'X-Auth-Email': CLOUDFLARE_EMAIL, 'X-Auth-Key': CLOUDFLARE_API, 'Content-Type': "application/json"}
CURRENT_IP           = ""
LAST_IP              = ""
###############################################################################################################################

import sys, subprocess
import json
import datetime, time

try:
    import requests
except:
    print("Requests lib not found", file=sys.stderr)
    print("pip install requests")
    subprocess.call([sys.executable, '-m', 'pip', 'install'] + "requests")
    try:
        import requests
    except:
        print("requests installation using pip failed!", file=sys.stderr)
        sys.exit(1)

CURRENT_IP = requests.get("https://api.ipify.org/")

if CURRENT_IP.status_code != 200:
    print("Couldn't get the current public ip of this machine.", file=sys.stderr)
    sys.exit(2)
else:
    CURRENT_IP = str(CURRENT_IP.text)

try:
	LAST_IP = open ("last.ip", 'r').read()
except: 
	pass

if str(LAST_IP) == str(CURRENT_IP):
	print ("IP not changed... exititng.. ")
	sys.exit(-1)

ATLEAST_SUCCESS = False
for i in range(0, len (CLOUDFLARE_SITES)):
    ENDPOINT   = CLOUDFLARE_ENDPOINT + ""
    ENDPOINT   = ENDPOINT.replace("{ZONE_ID}", CLOUDFLARE_SITES[i]["zone_id"])
    ENDPOINT   = ENDPOINT.replace("{DNS_ID}", CLOUDFLARE_SITES[i]["dns_id"])
    DNS_RECORD = {'type' : "A", 'name': CLOUDFLARE_SITES[i]["name"], 'content': CURRENT_IP}
    DNS_RECORD = json.dumps(DNS_RECORD)
    
    PUT = requests.put (ENDPOINT, data = DNS_RECORD, headers = CLOUDFLARE_HEADER)
    if PUT.status_code == 200:
        print ("IP updated for " + CLOUDFLARE_SITES[i]["name"] + " at " + str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        ATLEAST_SUCCESS = True
    else:
        print ("Failed to update " + CLOUDFLARE_SITES[i]["name"] + ". Status Code: " + str(PUT.status_code))
        print (PUT.content)

if ATLEAST_SUCCESS == True:
    open ("last.ip", 'w').write(CURRENT_IP)
    print("exiting...")
    sys.exit(0)

else:
    open ("last.ip", 'w').write("")
    sys.exit(3)