def caching_fibonacci():
    
    # Створюємо порожній словник для кешування результатів
    cache = {}
    
    def fibonacci(n):
        
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        # Перевіряємо, чи є значення в кеші
        if n in cache:
            return cache[n]
        
        # Обчислюємо та зберігаємо в кеші
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    
    # Повертаємо функцію
    return fibonacci
