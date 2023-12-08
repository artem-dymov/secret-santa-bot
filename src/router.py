import time
import asyncio
from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram import types
from aiogram.fsm.context import FSMContext

from src.keyboards import start_agreement_kb
from src.config import (start_cmd_message, registration_msg, pib_reg_msg, phone_number_req_msg,
                    nv_poshta_address_reg_msg, ukrposhta_index_reg_msg,  confirmation_reg_msg,
                    negative_confirmation_msg, positive_confirmation_msg, cancel_cmd_msg, wishes_msg)

from states import RegistrationForm

from src.db_api.db_manipulator import DatabaseManipulator
from src.validator import Validator

# def non_blocking_caller()
router = Router()


@router.message(Command('cancel'))
async def cancel_cmd(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(cancel_cmd_msg)


@router.message(Command('start'), StateFilter(None))
async def cmd_start(message: types.Message):
    await message.answer(text=start_cmd_message, reply_markup=start_agreement_kb)


@router.callback_query(F.data == 'initial_agreement', StateFilter(None))
async def initial_agreement(call: types.CallbackQuery, state: FSMContext):
    def find_user():
        dbm = DatabaseManipulator()
        usr = dbm.find_user({"tg_id": call.message.chat.id})
        del dbm
        return usr
    user = asyncio.get_event_loop().run_in_executor(None, find_user)

    if not user:
        await call.message.answer(f'{registration_msg}\n\n{pib_reg_msg}')
        await state.set_state(RegistrationForm.pib)
    else:
        await call.message.answer('Ви вже зареєстровані')

    await call.answer()


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
                             f'Індекс відділення Укрпошти: {user_data["ukrposhta_index"]}')
        await state.set_state(RegistrationForm.confirmation)
    else:
        await message.answer(val_res[1])


@router.message(RegistrationForm.confirmation)
async def reg_confirmation_enter(message: types.Message, state: FSMContext):
    match message.text.strip().lower():
        case 'так':
            user_data = await state.get_data()
            user_data.update({'tg_id': message.chat.id})

            def create_user():
                dbm = DatabaseManipulator()
                dbm.create_user(user_data)

            await asyncio.get_event_loop().run_in_executor(None, create_user)

            await message.answer(positive_confirmation_msg)
        case 'ні':
            await message.answer(negative_confirmation_msg)
        case _:
            await message.answer('Введіть тільки одне слово: Так бо Ні')

    await state.set_state(None)


