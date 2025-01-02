import asyncio
import time
from async_timeout import timeout

async def do_some_work(duration: int) -> str:
    """Імітує виконання роботи протягом заданого часу."""
    print(f"Початок роботи на {duration} секунд...")
    await asyncio.sleep(duration)
    print(f"Робота на {duration} секунд завершена.")
    return f"Результат роботи після {duration} секунд"

async def main():
    try:
        async with timeout(3):  # Скасувати, якщо робота триває довше 3 секунд
            result = await do_some_work(5)
            print(f"Отримано результат: {result}")
    except asyncio.TimeoutError:
        print("Роботу скасовано через перевищення часу.")

if __name__ == "__main__":
    asyncio.run(main())
