from src.ss_algorithm import assign_secret_santas


def test_secret_santa(users):
    pairs = assign_secret_santas(users)

    # Перевіряємо, чи є у кожного учасника Санта
    assert len(pairs) == len(users), "Не всі учасники мають Санту."

    # Перевіряємо, чи не є учасник своїм власним Сантою
    for user, santa in pairs.items():
        assert user != santa, f"{user} є своїм власним Сантою."

    # Перевіряємо, чи не є учасники взаємними Сантами
    for user, santa in pairs.items():
        assert pairs.get(santa) != user, f"{user} та {santa} є взаємними Сантами."

    print(f'pairs: {pairs}')
    print("Всі тести пройдено успішно!\n")

for i in range(100):
    test_secret_santa([1, 2, 3, 4, 5, 6, 7, 8])



