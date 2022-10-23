from aiogram import types


def edit_after_send_answers() -> types.InlineKeyboardMarkup:
    inline_kb_full: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
    inline_kb_full.add(
        types.InlineKeyboardButton(
            "Изменить 1", callback_data="edit_after_send_answers-1"
        ),
        types.InlineKeyboardButton(
            "Изменить 2", callback_data="edit_after_send_answers-2"
        ),
        types.InlineKeyboardButton(
            "Изменить 3", callback_data="edit_after_send_answers-3"
        ),
        types.InlineKeyboardButton(
            "Изменить 4", callback_data="edit_after_send_answers-4"
        ),
        types.InlineKeyboardButton(
            "Изменить 5", callback_data="edit_after_send_answers-5"
        ),
    )
    return inline_kb_full
