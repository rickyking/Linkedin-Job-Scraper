from scrapejobs import LinkedinScrap
import json


if __name__ == "__main__":
    # get config
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    username = config.get("username")
    # password = config.get('password')
    language = config.get("language")
    position = config.get("position")
    location = config.get("location")
    max_jobs = config.get("max_jobs")

    # print input
    print("\ninput:")

    print(
        "\nUsername:  " + username,
        "\nPassword:  " + password,
        "\nLanguage:  " + language,
        "\nPosition:  " + position,
        "\nLocation:  " + location,
    )

    print("\nLet's scrape some jobs!\n")

    # start
    bot = LinkedinScrap(username, password, language, position, location, max_jobs)
    bot.start_scrape()
