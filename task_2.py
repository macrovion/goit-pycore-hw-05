import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    
    # Пошук дійсних чисел
    pattern = r'\b\d+(?:\.\d+)?\b'
    
    # Знаходимо всі збіги в тексті
    matches = re.findall(pattern, text)
    
    # Повертаємо кожне число як float через yield
    for match in matches:
        yield float(match)


def sum_profit(text: str, func: Callable) -> float:
    
    # Використовуємо генератор для отримання чисел та підсумовуємо їх
    total = sum(func(text))
    return total
