class Validator:
    @classmethod
    def val_phone_number(cls, phone_num: str) -> list[bool, str]:
        try:
            int(phone_num.strip())
        except Exception as e:
            return [False, 'Ви маєте вводити тільки цифри без пробілів']

        l = len(str(phone_num))
        if l < 12:
            return [False, f'Мало цифр для телефонного номера: {l}. Пишіть номер у міжнародному форматі, '
                           f'+ не використовуйте']
        elif l > 12:
            return [False, f'Забагато цифр для телефонного номера: {l}. Пишіть номер у міжнародному форматі, '
                           f'+ не використовуйте']

        return [True, 'Валідація успішна']

    @classmethod
    def val_str_len(cls, text: str) -> list[bool, str]:
        if len(text) > 150:
            return [False, f'Завелике повідомлення: {len(text)} символів, має бути до 150']
        else:
            return [True, f'Валідація успішна']


    @classmethod
    def val_index(cls, ind: str):
        l = len(ind)

        try:
            ind = int(ind.strip())
        except Exception as e:
            return [False, 'Ви маєте вводити тільки цифри без пробілів']

        if l != 5:
            return [False, f'Помилка. У індексі має бути 5 цифр']

        return [True, 'Валідація успішна']