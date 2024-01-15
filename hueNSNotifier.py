from time import sleep
from phue import Bridge
from nslookup import Nslookup

######### MODIFY AS NECESSARY #########

HUE_BRIDGE_IP = "192.0.2.0"

DEFAULT_DOMAIN = "abkslm.com"

ALERT_HUE = 43690

LIGHT_NAME = "Desk Lamp"

######### 

hue = Bridge(HUE_BRIDGE_IP)
hue.connect() #### MUST PRESS HUE BRIDGE BUTTON < 30S BEFORE RUNNING #### 

light_objs = hue.get_light_objects('name')
light = light_objs[LIGHT_NAME]

domain = input("Please enter a domain to resolve (or press enter for default): ")

if not domain:
    domain = DEFAULT_DOMAIN
    
dns_query = Nslookup(dns_servers=["1.1.1.1"], verbose=False)
ip_lookup = dns_query.dns_lookup(domain)

print("Attempting to resolve", domain, "\n")


while (not ip_lookup.response_full):
    print(domain, "could not be resolved...")
    print("Maintaining state for Hue light \"", light.name, "\"", sep='')
    
    print("Sleeping for 30 seconds", end="")
    for i in range(30):
        print(".", sep='', end='', flush=True)
        
        if (i % 5 == 0) and (i != 0):
            print(30 - i, sep='', end='', flush=True)
            
        sleep(1)
        
    dotLine = "." * 50
    print("\n", dotLine, "\n", sep='')
    
    ip_lookup = dns_query.dns_lookup(domain)

if(ip_lookup.response_full):
    print("Resolved ", domain, "!", sep="")
    print("Beginning Hue alert!")

    # first get original settings
    ogPow = light.on
    ogHue = light.hue
    ogSat = light.saturation
    ogBri = light.brightness

    # now, update to alert color
    light.on = True
    light.transitiontime = 1
    light.hue = ALERT_HUE
    light.saturation = 254
    light.brightness = 0

    # Flash
    for i in range(5):
        light.brightness = 254
        sleep(0.25)
        
        light.brightness = 0
        sleep(0.25)

    # Reset lights to original state
    light.on = ogPow
    light.hue = ogHue
    light.saturation = ogSat
    light.brightness = ogBri
    light.transitiontime = None
