import Constants
import ThemeBot
import DataPacket
from Utils import IO


TOKEN = "YourToken"


def init():
    data = IO.read_file_json(Constants.DATA_PATH + Constants.DATA_MEMBERS_FILENAME)
    if data != 0:
        DataPacket.members = data
        if len(DataPacket.members) != 0:
            DataPacket.is_process_started = True

def main():
    init()
    bot = ThemeBot.ThemeBot(TOKEN)
    bot.start_bot()


if __name__ == '__main__':
    main()