from aiogram import Router
from aiogram import types
import config

from src.db_api.DbManipulator import DbManipulator
from src.validator import Validator
from config import all_msg_after_reg
from src.bot import bot

from src.ss_algorithm import assign_secret_santas

# def non_blocking_caller()
router_after_reg = Router()
dbm = DbManipulator()


@router_after_reg.message()
async def all_msg_handler(message: types.Message):
    if message.from_user.id == config.admin_id:
        if message.text == '/set':
            users = await dbm.get_all_users()
            users_ids = []
            for user in users:
                users_ids.append(user.id)

            pairs = assign_secret_santas(users_ids)
            flag_all_ok = True
            for user_id, santa_id in pairs.items():
                result1 = await dbm.update_santa(user_id, santa_id)
                result2 = await dbm.update_user_to_gift(santa_id, user_id)
                if not result1 or not result2:
                    flag_all_ok = False

            if flag_all_ok:
                await message.answer('Розподіл виконано успішно!')
            else:
                await message.answer('Проблема при розподілі!')
        elif message.text == '/send':
            users = await dbm.get_all_users()
            for user in users:
                user_to_gift = await dbm.find_user({'id': user.user_to_gift_id})
                try:
                    await bot.send_message(user.tg_id, f'{config.last_msg}'
                                                       f'ПІБ: {user_to_gift.pib}\n'
                                                       f'Номер телефону: {user_to_gift.phone_number}\n'
                                                       f'Адрес відділення Нової пошти або поштомату: '
                                                       f'{user_to_gift.nv_poshta_address}\n'
                                                       f'Індекс відділення Укрпошти: {user_to_gift.ukrposhta_index}\n'
                                                       f'Ваші побажання: {user_to_gift.wishes}'
                    )
                except Exception as e:
                    print(e)
        elif message.text == '/reveal':
            users = await dbm.get_all_users()
            for user in users:
                santa = await dbm.find_user({'id': user.santa_id})

                try:
                    await bot.send_message(user.tg_id, f'Кінцева дата надсилання подарунків пройшла.\n'
                                                       f'Оце собсна дані Вашого Санти, якщо він Вам нічого не прислав, то Ви знаєте кому начистити їбальничок\n\n'
                                                       f'ПІБ: {santa.pib}\n'
                                                       f'Номер телефону: {santa.phone_number}\n'
                                                       f'Адрес відділення Нової пошти або поштомату: '
                                                       f'{santa.nv_poshta_address}\n'
                                                       f'Індекс відділення Укрпошти: {santa.ukrposhta_index}\n'
                                           )
                except Exception as e:
                    print(e)

    else:
        await message.answer(all_msg_after_reg)

