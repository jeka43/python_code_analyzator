import inspect
import requests
from g4f.client import Client

class InvalidTokenError(Exception):
    """Исключение для недействительных токенов."""
    pass


def check_token(token):
    """
    Проверяет токен через сервер проверки.
    :param token: str - токен для проверки
    :return: dict - информация о токене (например, оставшиеся запросы)
    :raises InvalidTokenError: если токен недействителен
    """
    server_url = "http://192.168.0.148:5000/check"  # Укажите IP-адрес сервера
    try:
        response = requests.post(server_url, json={"token": token})
        if response.status_code == 200:
            token_data = response.json()
            remaining_requests = token_data.get("remaining_requests", 0)
            print(f"Ваша подписка действует. Осталось запросов: {remaining_requests}")
            return token_data
        elif response.status_code == 403:
            print("Токен недействителен или лимит запросов исчерпан.")
            raise InvalidTokenError("Токен недействителен или не существует.")
        else:
            raise InvalidTokenError("Неизвестная ошибка проверки токена.")
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка соединения с сервером проверки токенов: {e}")


def extract_code(target):
    """
    Извлекает текст кода из функции, строки или файла.
    :param target: callable или str - функция, строка с кодом или путь к файлу
    :return: str - текст кода
    """
    if callable(target):
        return "".join(inspect.getsourcelines(target)[0])
    elif isinstance(target, str):
        try:
            with open(target, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {target} не найден.")
    else:
        raise TypeError("Ожидалась функция, строка с кодом или путь к файлу.")


def analyze_code_with_gpt(target, token):
    """
    Платная функция. Анализирует код с использованием нейросети.
    :param target: callable или str - функция, строка с кодом или путь к файлу
    :param token: str - токен доступа
    :return: str - результат анализа
    """
    token_data = check_token(token)  # Проверяем токен и получаем информацию
    remaining_requests = token_data.get("remaining_requests", "неизвестно")
    if remaining_requests != "неизвестно" and remaining_requests > 0:
        remaining_requests -= 1
    code = extract_code(target)
    client = Client()
    prompt = (
        f"Проанализируй следующий Python-код и укажи ошибки, которые могут нарушить выполнение программы. "
        f"Не обращай внимания на ошибки, связанные с директориями и наличием файлов, они заведомо исправны. "
        f"Укажи их в формате: 'Строка X: описание ошибки'. "
        f"Если ошибок нет, напиши, что код исправен. Ответь на русском языке:\n\n{code}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"Осталось запросов: {remaining_requests}")
    return response.choices[0].message.content


def suggest_fixes_with_gpt(target, token):
    """
    Платная функция. Предлагает исправления для найденных ошибок.
    :param target: callable или str - функция, строка с кодом или путь к файлу
    :param token: str - токен доступа
    :return: str - рекомендации по исправлению
    """
    token_data = check_token(token)  # Проверяем токен и получаем информацию
    remaining_requests = token_data.get("remaining_requests", "неизвестно")
    if remaining_requests != "неизвестно" and remaining_requests > 0:
        remaining_requests -= 1
    code = extract_code(target)
    client = Client()
    prompt = (
        f"Проанализируй следующий Python-код и предложи исправления. "
        f"Если ошибок нет, напиши, что код исправен. "
        f"Ответь на русском языке:\n\n{code}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"Осталось запросов: {remaining_requests}")
    return response.choices[0].message.content


def generate_fixed_code_with_gpt(target, token, output_file="fixed_code.py"):
    """
    Генерирует исправленный код с использованием нейросети и сохраняет его в файл.
    :param target: callable или str - функция, строка с кодом или путь к файлу
    :param token: str - токен доступа
    :param output_file: str - имя файла для сохранения
    """
    token_data = check_token(token)  # Проверяем токен и получаем информацию
    remaining_requests = token_data.get("remaining_requests", "неизвестно")
    if remaining_requests != "неизвестно" and remaining_requests > 0:
        remaining_requests -= 1
    code = extract_code(target)
    client = Client()
    prompt = (
        f"Исправь следующий Python-код и предоставь только исправленный код без комментариев и пояснений:\n\n{code}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    # Убираем кавычки и элементы ```python из начала и конца результата
    fixed_code = response.choices[0].message.content
    fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

    # Сохраняем исправленный код в указанный файл
    with open(output_file, "w") as file:
        file.write(fixed_code)
    print(f"Файл успешно сохранен! Осталось запросов: {remaining_requests}")


def check_code_pep8(target):
    """
    Бесплатная функция. Проверяет код на соответствие PEP8 через нейросеть.
    :param target: callable или str - функция, строка с кодом или путь к файлу
    :return: str - рекомендации по улучшению стиля
    """
    code = extract_code(target)
    client = Client()
    prompt = (
        f"Проанализируй следующий Python-код и укажи, соответствует ли он стандарту PEP8. "
        f"Если есть несоответствия, укажи их с рекомендациями по исправлению. "
        f"Ответь на русском языке:\n\n{code}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
