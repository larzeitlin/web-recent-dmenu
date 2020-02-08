#!/usr/bin/python3

import sqlite3
import os
import shutil
import re

def copy_db(location):
    destination = os.path.expanduser("~") + "/.firefox_places_copy.sqlite"
    if os.path.exists(destination):
        os.remove(destination)
    shutil.copy2(location, destination)
    return(destination)

def get_profile_name():
    profiles_path = os.path.expanduser('~')+"/.mozilla/firefox/profiles.ini"
    with open(profiles_path) as p:
        lines = p.readlines()
        profile_matches = [re.search(r"^Path=(.*\.default)$", l).group(1)
                           for l in lines if l.startswith( 'Path' )]
        profile = profile_matches.pop()
        return(profile)
        
def main():
    profile_name = get_profile_name()
    places_path = os.path.expanduser('~')+"/.mozilla/firefox/{}/places.sqlite".format(profile_name)
    db = copy_db(places_path)
    c = sqlite3.connect(db)
    cursor = c.cursor()
    select_statement = "select moz_places.url, moz_places.visit_count from moz_places order by moz_places.visit_count desc;"
    cursor.execute(select_statement)
    results = cursor.fetchall()
    print("\n".join([r[0] for r in results]))

if __name__ == "__main__":
    main()
