from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    pib = State()
    phone_number = State()
    nv_poshta_address = State()
    ukrposhta_index = State()
    wishes = State()
    confirmation = State()