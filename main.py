from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from utils.shedule_parsing import start_schedule
from multiprocessing import Process

if __name__ == "__main__":
    # Process(target=start_schedule(), args=()).start()
    set_default_commands(bot)
    bot.infinity_polling()
