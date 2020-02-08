#!/usr/bin/python3

import sqlite3
import os
import shutil

def copy_db(location):
    destination = os.path.expanduser("~") + "/.firefox_places_copy.sqlite"
    if os.path.exists(destination):
        os.remove(destination)
    shutil.copy2(location, destination)
    return(destination)

def main():
    places_path = os.path.expanduser('~')+"/.mozilla/firefox/7r5u8o5y.default/places.sqlite"
    db = copy_db(places_path)
    c = sqlite3.connect(db)
    cursor = c.cursor()
    select_statement = "select moz_places.url, moz_places.visit_count from moz_places order by moz_places.visit_count desc;"
    cursor.execute(select_statement)
    results = cursor.fetchall()
    print("\n".join([r[0] for r in results]))

if __name__ == "__main__":
    main()
