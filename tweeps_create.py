import snscrape.modules.twitter


def create_tweeps():
    """Create a file to list of users to follow. The argument will be
    the user id, as we might loose track of the user when
    the user decides to change his / hers username.
    Also write usernames back from user ids for those mentioned
    username changes.

    :returns: List of user ids

    :rtype: List
    """

    with open("tweeps.py", "w") as f:
        f.write("import utils\n")
        f.write("import snscrape.modules.twitter\n\n\n")
        f.write("def tweeps():\n")
        f.write("\tusers = [\n")
        with open("tweeps.txt") as userlist:
            for user in userlist:
                user = user.rstrip("\n")
                print(user)
                temp = snscrape.modules.twitter.TwitterUserScraper(user)
                naam = temp.entity.id
                f.write(f'\t\t"{naam}",\n')
        f.write("\t]\n\n")
        f.write("\treturn users")
        f.write("\n\n")
        f.write("class Tweeps:\n")
        f.write("\tdef listconvert():\n")
        f.write("\t\tusernames = []\n")
        f.write("\t\tuserlist = tweeps()\n")
        f.write('\t\twith open("tweepsnieuw.txt", "w") as nieuw:\n')
        f.write("\t\t\tfor user in userlist:\n")
        f.write("\t\t\t\ttry:\n")
        f.write(
            "\t\t\t\t\tscraper = snscrape.modules.twitter.TwitterUserScraper(int(user))\n"
        )
        f.write("\t\t\t\t\tscraper = scraper.entity.username\n")
        f.write('\t\t\t\t\tnieuw.write(scraper + "\\n")\n')
        f.write("\t\t\t\t\tusernames.append(scraper)\n")
        f.write("\t\t\t\texcept Exception as e:\n")
        f.write(
            '\t\t\t\t\tutils.log_debug(f"[LOGGING]Failed to retrieve username: {e}")\n\n'
        )
        f.write('\t\tutils.log_debug(f"[LOGGING]Following: {usernames}")\n')
        f.write("\t\treturn usernames")


create_tweeps()
