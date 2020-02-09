#!/usr/bin/env python3

import re
import shutil
import sqlite3
import tempfile
import configparser
from pathlib import Path


FIREFOX_HOME = Path.home() / ".mozilla/firefox"


def sqlite_regexp(pattern, string):
    return re.search(pattern, string) != None


def copy_db(location):
    destination = Path(tempfile.mkstemp()[1])
    shutil.copy2(str(location), str(destination))

    return destination


def get_profile_name():
    config = configparser.ConfigParser()
    config.read(FIREFOX_HOME / "profiles.ini")
    # 99% of the time this will be your profile
    profile = config["Profile0"]["Path"]

    # but just in case:
    profiles = [
        section for section in list(config.keys()) if section.startswith("Profile")
    ]
    if profiles and len(profile) > 1:
        for name in profiles:
            if config[name]["Default"] == 1:
                profile = config[name]["Path"]
                break

    return profile


def select_recent(db_file):
    conn = sqlite3.connect(db_file)
    conn.create_function("REGEXP", 2, sqlite_regexp)
    cursor = conn.cursor()
    select_statement = (
        "SELECT DISTINCT RTRIM(url,'/') "
        "FROM moz_places "
        "WHERE url REGEXP '^(.*):\/\/' "
        "ORDER BY moz_places.visit_count DESC"
    )
    cursor.execute(select_statement)
    result = cursor.fetchall()
    cursor.close()

    return result


def main():
    profile_name = get_profile_name()
    db_file = copy_db(FIREFOX_HOME / f"{profile_name}/places.sqlite")
    results = select_recent(db_file)

    print("\n".join([row[0] for row in results]))
    db_file.unlink()


if __name__ == "__main__":
    main()
