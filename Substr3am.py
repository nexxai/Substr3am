#!/usr/local/bin/python3

####################
#   Substr3am v1.0
#
#   @nexxai
#   github.com/nexxai/Substr3am
####################

import sys
import certstream
import tldextract
import re
import argparse

from sqlalchemy import create_engine
from declarative_sql import Subdomain, Base
from sqlalchemy.orm import sessionmaker

def print_callback(message, context):
    # Add any subdomains (or partial strings) you want to ignore here
    subdomains_to_ignore = [
        "www",
        "*",
        "azuregateway",
        "direwolf",
        "devshell-vm-",
        "device-local",
        "-local",
        "sni"
    ]

    subdomains_regex_to_ignore = [
        # 81d556ba781237c92f0c410f
        "[a-f0-9]{24}",                         
        
        # device1650096-3a628f22
        "device[a-f0-9]{7}-[a-f0-9]{8}",
        
        # e4751426-33f2-4239-9765-56b4cbcb505d
        "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",

        #device-3e90cd1b-50dc-48f1-90ac-6389856ccb2e
        "device-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
    ]

    if message['message_type'] == "heartbeat":
        return

    # These are the messages we care about
    if message['message_type'] == "certificate_update":
        # Some certificates have SAN addresses attached to them
        # so we want to know about all of them
        domains = message['data']['leaf_cert']['all_domains']

        for domain in domains:
            # Use the tldextract library to break the domain into its parts
            extract = tldextract.extract(domain)
            # But we only care about the subdomain
            subdomain = extract.subdomain

            # Make sure there's actually something there
            if len(subdomain) > 0:

                # Sometimes extract.subdomain gives us something like "www.testing.box"
                # so search for anything with a period in it
                multi_level = subdomain.find(".")

                # If it find something that has a period in it...
                if multi_level != -1:
                    # Split it into two parts, the "www" and the "testing.box"...
                    subdomain_split = subdomain.split('.', 1)
                    # ...and we only care about the first entry
                    subdomain = subdomain_split[0]  

                i = 0
                # See if any of the subdomains_to_ignore are substrings of the one we're checking
                # e.g. "devshell-vm" is a substring of "devshell-vm-0000-0000-00000000"
                for search in subdomains_to_ignore:
                    # If it matches, increase the counter
                    if search in subdomain:
                        i += 1
                
                # See if any of the subdomains_regex_to_ignore are substrings of the one we're checking
                for search in subdomains_regex_to_ignore:
                    # If it matches, increase the counter
                    if re.search(search, subdomain):
                        i += 1

                # As long as none of the substrings or regexes match, continue on
                if i == 0:
                    # Set up the connection to the sqlite db
                    engine = create_engine('sqlite:///subdomains.db')
                    Base.metadata.bind = engine
                    Session = sessionmaker()
                    Session.configure(bind=engine)
                    session = Session()

                    # Check to see if it already exists in the database...
                    subdomain_exists = session.query(Subdomain).filter_by(subdomain=subdomain).first()
                    
                    # It doesn't exist...
                    if not subdomain_exists:
                        # ...so create it
                        subdomain_new = Subdomain(subdomain=subdomain)
                        session.add(subdomain_new)
                        session.commit()

                        # Debug line
                        print(subdomain)

def dump():
    # Set up the connection to the sqlite db
    engine = create_engine('sqlite:///subdomains.db')
    Base.metadata.bind = engine
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Get all the subdomains
    subdomains = session.query(Subdomain).all()
    if len(subdomains) > 0:
        f = open("names.txt", "w")
        for subdomain in subdomains:
            # And write them to a file
            f.write(subdomain.subdomain)
            f.write("\r\n")
        f.close()
    sys.exit('names.txt has been written')


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--dump', help="Dump the list of collected subdomains to names.txt", action='store_true')
    return parser.parse_args()

def parser_error(errmsg):
    banner()
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()

def main():
    # Actually connect to the certstream firehose, and listen for events
    certstream.listen_for_events(print_callback)

def interactive():
    args = parse_args()

    if args.dump:
        dump()

    banner()
    main()

def banner():
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white

    print("""%s
  _________    ___.             __        ________                 
 /   _____/__ _\_ |__   _______/  |_______\_____  \_____    _____  
 \_____  \|  |  \ __ \ /  ___/\   __\_  __ \_(__  <\__  \  /     \ 
 /        \  |  / \_\ \\\\___ \  |  |  |  | \/       \/ __ \|  Y Y  \\
/_______  /____/|___  /____  > |__|  |__| /______  (____  /__|_|  /
        \/          \/     \/                    \/     \/      \/ %s%s

                # Coded By Justin Smith - @nexxai
    """ % (R, W, Y))

if __name__ == "__main__":
    interactive()
