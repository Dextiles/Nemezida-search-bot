from telebot.types import Message
from keyboards.inline import show_instruction as show_instruction_btn
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text),
                 reply_markup=show_instruction_btn.get_show_instruction_button())
