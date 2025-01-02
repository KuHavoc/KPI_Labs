import asyncio
import time

async def do_some_work(duration: int) -> str:
    """Імітує виконання роботи протягом заданого часу."""
    print(f"Початок роботи на {duration} секунд...")
    await asyncio.sleep(duration)
    print(f"Робота на {duration} секунд завершена.")
    return f"Результат роботи після {duration} секунд"

async def main():
    result = await do_some_work(5)
    print(f"Отримано результат: {result}")

if __name__ == "__main__":
    asyncio.run(main())
