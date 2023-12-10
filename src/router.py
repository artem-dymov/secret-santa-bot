from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram import types
from aiogram.fsm.context import FSMContext

from src.keyboards import start_agreement_kb, cancel_reg_kb
from src.config import (start_cmd_message, registration_msg, pib_reg_msg, phone_number_req_msg,
                    nv_poshta_address_reg_msg, ukrposhta_index_reg_msg,  confirmation_reg_msg,
                    negative_confirmation_msg, positive_confirmation_msg, cancel_cmd_msg, wishes_msg,
                    cancel_reg_cmd_msg)

from states import RegistrationForm

from src.db_api.DbManipulator import DbManipulator
from src.validator import Validator

# def non_blocking_caller()
router = Router()
dbm = DbManipulator()


@router.message(Command('cancel'))
async def cancel_cmd(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(cancel_cmd_msg)


@router.message(Command('start'), StateFilter(None))
async def cmd_start(message: types.Message):
    await message.answer(text=start_cmd_message, reply_markup=start_agreement_kb)


@router.callback_query(F.data == 'initial_agreement', StateFilter(None))
async def initial_agreement(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(None)

    user = await dbm.find_user({"tg_id": call.message.chat.id})

    if not user:
        await call.message.answer(f'{registration_msg}\n\n{pib_reg_msg}')
        await state.set_state(RegistrationForm.pib)
    else:
        await call.message.answer('Ви вже зареєстровані')

    await call.answer()


@router.callback_query(F.data.startswith('cancel_reg'), StateFilter(None))
async def cancel_reg(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(None)

    user = await dbm.find_user({"tg_id": call.message.chat.id})
    if not user:
        await call.message.answer(f'Ви не зареєстровані')
    else:
        # var "choice", type - int. 1 - Yes, 0 - No
        choice = int(call.data.split(':')[1])
        if choice == 1:
            result = await dbm.delete_user(user.id)
            if result:
                await call.message.answer('Вас було видалено з гри')
            else:
                await call.message.answer('Помилка! Не вдалося виконати операцію! Зверніться до боту підтримки у біо')
        elif choice == 0:
            await call.message.answer('Відміна реєстрації скасована')

    await call.answer()


@router.message(Command('cancel_reg'))
async def cancel_reg_cmd(message: types.Message, state: FSMContext):
    if await state.get_state():
        await message.answer('Не можна вийти з гри під час реєстрації (\n\nНатисніть /cancel, щоб скасувати реєстрацію')
    else:
        await message.answer(cancel_reg_cmd_msg, reply_markup=cancel_reg_kb)


@router.message(RegistrationForm.pib, F.text)
async def pib_enter(message: types.Message, state: FSMContext):
    val_res: list = Validator.val_str_len(message.text)

    if val_res[0]:
        await state.update_data({'pib': message.text})
        await message.answer(phone_number_req_msg)
        await state.set_state(RegistrationForm.phone_number)
    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.phone_number)
async def phone_number_enter(message: types.Message, state: FSMContext):

    val_res: list = Validator.val_phone_number(message.text)

    if val_res[0]:
        await state.update_data({'phone_number': message.text})
        await message.answer(nv_poshta_address_reg_msg)
        await state.set_state(RegistrationForm.nv_poshta_address)

    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.nv_poshta_address)
async def nv_poshta_address_enter(message: types.Message, state: FSMContext):
    val_res: list = Validator.val_str_len(message.text)
    if val_res[0]:
        await state.update_data({'nv_poshta_address': message.text})
        await message.answer(ukrposhta_index_reg_msg)
        await state.set_state(RegistrationForm.ukrposhta_index)
    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.ukrposhta_index)
async def ukrposhta_index_enter(message: types.Message, state: FSMContext):
    val_res: list = Validator.val_index(message.text)
    if val_res[0]:
        await state.update_data({'ukrposhta_index': message.text})
        await message.answer(wishes_msg)
        await state.set_state(RegistrationForm.wishes)
    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.wishes)
async def wishes_enter(message: types.Message, state: FSMContext):
    val_res: list = Validator.val_str_len(message.text)
    if val_res[0]:
        await state.update_data({'wishes': message.text})

        user_data = await state.get_data()
        await message.answer(f'{confirmation_reg_msg}\n\n'
                             f'Ваш ПІБ: {user_data["pib"]}\n'
                             f'Ваш номер телефону: {user_data["phone_number"]}\n'
                             f'Адрес відділення Нової пошти: {user_data["nv_poshta_address"]}\n'
                             f'Індекс відділення Укрпошти: {user_data["ukrposhta_index"]}\n'
                             f'Ваші побажання: {user_data["wishes"]}')
        await state.set_state(RegistrationForm.confirmation)
    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.confirmation)
async def reg_confirmation_enter(message: types.Message, state: FSMContext):
    match message.text.strip().lower():
        case 'так':
            user_data = await state.get_data()
            user_data.update({'tg_id': message.chat.id})

            await dbm.create_user(user_data)

            await message.answer(positive_confirmation_msg)
        case 'ні':
            await message.answer(negative_confirmation_msg)
        case _:
            await message.answer('Введіть тільки одне слово: Так бо Ні')

    await state.set_state(None)


