from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.utils.markdown import hcode

from src.loader import dp
from src.i18n import _
from src.keys import TextKeys, TextKeyBuilder


@dp.message_handler(text_key=TextKeys.MAIN_MENU, state="*", )
@dp.message_handler(CommandStart(), state="*")
async def start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)

    keyboard: types.ReplyKeyboardMarkup = TextKeyBuilder(
        resize_keyboard=True, input_field_placeholder=_("main_menu_placeholder"), is_persistent=True
    )
    keyboard.add(TextKeys.FIND_EXERCISE)
    keyboard.add(TextKeys.GET_PROGRAM)
    # keyboard.add(TextKeys.GET_INDIVIDUAL_PROGRAM)

    await message.answer(
        _("entry_welcome_message {full_name}").format(full_name=message.from_user.full_name),
        reply_markup=keyboard
    )


@dp.message_handler(Command("test"), state="*")
async def test(message: types.Message,):
    await message.answer(_("entry_test"), )


@dp.message_handler(Command("id"), state="*")
async def get_chat_id(message: types.Message):
    await message.answer(f"{_('entry_your_chat_id')}: {hcode(message.from_user.id)}", )
