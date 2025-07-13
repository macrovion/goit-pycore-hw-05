import sys
import os
from typing import Dict, List, Optional

#Парсить рядок логу та повертає словник з компонентами 
def parse_log_line(line: str) -> Dict[str, str]:
    
    line = line.strip()
    if not line:
        return {}
    
    parts = line.split(' ', 3)  # Розділяємо на максимум 4 частини
    
    if len(parts) < 4:
        return {}
    
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': parts[3]
    }

# Завантажує логи з файлу та парсить кожен рядок
def load_logs(file_path: str) -> List[Dict[str, str]]:
    
    logs = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                parsed_log = parse_log_line(line)
                if parsed_log:  # Додаємо тільки коректні записи
                    logs.append(parsed_log)
                elif line.strip():  # Повідомляємо про некоректнтні рядки
                    print(f"Попередження: Невалідний формат у рядку {line_num}: {line.strip()}")
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не знайдено")
    except IOError as e:
        raise IOError(f"Помилка при читанні файлу '{file_path}': {e}")
    
    return logs


# Фільтрує логи за рівнем логування
def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    
    # Використовуємо функцію filter та лямбда-функцію
    return list(filter(lambda log: log.get('level', '').upper() == level.upper(), logs))


# Підраховує кількість записів для кожного рівня логування
def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    
    counts = {}
    
    # Використовуємо списковий вираз
    levels = [log.get('level', '') for log in logs if log.get('level')]
    
    for level in levels:
        counts[level] = counts.get(level, 0) + 1
    
    return counts


# Виводить результати підрахунку в форматі таблиці
def display_log_counts(counts: Dict[str, int]) -> None:
    
    if not counts:
        print("Немає даних для відображення")
        return
    
    print("\nРівень логування | Кількість")
    print("-" * 30)
    
    # Сортуємо рівні за кількістю записів
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    for level, count in sorted_counts:
        print(f"{level:<15} | {count}")


# Виводить детальну інформацію для відфільтрованих логів
def display_filtered_logs(logs: List[Dict[str, str]], level: str) -> None:
    
    if not logs:
        print(f"\nНемає записів для рівня '{level.upper()}'")
        return
    
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    
    # Перевірка аргументів командного рядка
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу_логів> [рівень_логування]")
        print("Приклад: python main.py /path/to/logfile.log")
        print("Приклад: python main.py /path/to/logfile.log error")
        sys.exit(1)
    
    file_path = sys.argv[1]
    filter_level = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Перевірка існування файлу
    if not os.path.exists(file_path):
        print(f"Помилка: Файл '{file_path}' не існує")
        sys.exit(1)
    
    try:
        # Завантаження логів
        print(f"Завантаження логів з файлу: {file_path}")
        logs = load_logs(file_path)
        
        if not logs:
            print("Файл не містить валідних записів логів")
            sys.exit(1)
        
        print(f"Завантажено {len(logs)} записів логів")
        
        # Підрахунок статистики
        counts = count_logs_by_level(logs)
        
        # Виведення загальної статистики
        display_log_counts(counts)
        
        # Якщо вказано рівень фільтрації, виводимо деталі
        if filter_level:
            filtered_logs = filter_logs_by_level(logs, filter_level)
            display_filtered_logs(filtered_logs, filter_level)
        
    except FileNotFoundError as e:
        print(f"Помилка: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Помилка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неочікувана помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
