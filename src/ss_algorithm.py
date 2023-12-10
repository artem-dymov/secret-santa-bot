import random

def assign_secret_santas(users):
    # Перевіряємо, чи достатньо учасників для розподілу
    if len(users) < 3:
        return "Потрібно мінімум 3 учасники для розподілу."

    # Створюємо копію списку учасників
    available_santas = users.copy()
    random.shuffle(available_santas)

    # Створюємо словник для зберігання пар
    pairs = {}

    for i in range(len(users)):
        # Перевіряємо, чи не є поточний Санта тим самим учасником
        # або чи не є він вже призначеним цьому учаснику
        if users[i] != available_santas[i] and available_santas[i] not in pairs.values():
            pairs[users[i]] = available_santas[i]
        else:
            # Якщо учасник і Санта співпадають, або Санта вже призначена,
            # то ми обмінюємо Санту з наступним учасником у списку
            next_index = (i + 1) % len(users)
            pairs[users[i]], pairs[users[next_index]] = available_santas[next_index], available_santas[i]

    # Перевіряємо, чи не є учасники взаємними Сантами
    for user, santa in pairs.items():
        if pairs.get(santa) == user:
            return assign_secret_santas(users)

    return pairs

