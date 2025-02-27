from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
balances = {}

class RegSum(StatesGroup):
    money = State()
    minus = State()


@router.message(CommandStart())
async def help_cmd(message: Message):
    await message.answer('Здраствуй это Telegram бот по учету финансов \nВот список команд для пользователя: \n'
                         '1. /vnesti - вносим некую сумму \n'
                         '2. /min - вычитаем некую сумму \n'
                         '3. /sum - информация о сумме сбережений')


@router.message(Command('vnesti'))
async def vnesti_set(message: Message, state: FSMContext):
    await state.set_state(RegSum.money)
    await message.answer('Введите сумму, которую хотите внести:')


@router.message(RegSum.money)
async def vnesti_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        balances[user_id] = balances.get(user_id, 0) + amount
        await message.answer(f'Сумма {amount}р. успешно внесена! Ваш баланс: {balances[user_id]}р.')
        await state.clear()
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')

@router.message(Command('min'))
async def min_set(message: Message, state: FSMContext):
    await state.set_state(RegSum.minus)
    await message.answer('Введите сумму, которую хотите вычесть:')

@router.message(RegSum.minus)
async def min_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        if user_id not in balances or balances[user_id] < amount:
            await message.answer('Недостаточно средств на балансе!')
        else:
            balances[user_id] -= amount
            await message.answer(f'Сумма {amount}р. успешно вычтена! Остаток: {balances[user_id]}р.')
        await state.clear()
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число.')

@router.message(Command('sum'))
async def sum_cmd(message: Message):
    user_id = message.from_user.id
    balance = balances.get(user_id, 0)
    await message.answer(f'Ваш текущий баланс: {balance}р.')
