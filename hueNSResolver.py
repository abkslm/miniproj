from time import sleep
from phue import Bridge
from nslookup import Nslookup

hue = Bridge("192.168.88.177")

domain = "repo.maven.apache.org"

light_objs = hue.get_light_objects('name')
desk = light_objs["Desk Lamp"]

dns_query = Nslookup(dns_servers=["1.1.1.1"], verbose=True)

userDomain = input("Please enter a domain to resolve (or press enter for default): ")

if userDomain:
    domain = userDomain

ip_lookup = dns_query.dns_lookup(domain)

print("Attempting to resolve", domain, "\n")

while (not ip_lookup.response_full):
    print(domain, "could not be resolved...")
    print("Maintaining state for Hue light \"", desk.name, "\"", sep='')
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
    ogPow = desk.on
    ogHue = desk.hue
    ogSat = desk.saturation
    ogBri = desk.brightness

    # now, update to bright red
    desk.on = True
    desk.transitiontime = 1
    desk.hue = 43690
    desk.saturation = 254
    desk.brightness = 0

    # Flash red
    for i in range(5):
        desk.brightness = 254
        sleep(0.25)
        desk.brightness = 0
        sleep(0.25)

    # Reset lights to original state
    desk.on = ogPow
    desk.hue = ogHue
    desk.saturation = ogSat
    desk.brightness = ogBri
    desk.transitiontime = None