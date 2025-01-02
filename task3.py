import asyncio
import time
from async_timeout import timeout

async def do_some_work(duration: int, cancel_event: asyncio.Future) -> str:
    """Імітує виконання роботи протягом заданого часу."""
    print(f"Початок роботи на {duration} секунд...")
    try:
        await asyncio.wait_for(asyncio.sleep(duration), timeout=None, future=cancel_event)
        print(f"Робота на {duration} секунд завершена.")
        return f"Результат роботи після {duration} секунд"
    except asyncio.CancelledError:
        print("Роботу скасовано ззовні.")
        raise

async def main():
    cancel_event = asyncio.Future()
    try:
        task = asyncio.create_task(do_some_work(5, cancel_event))
        await asyncio.sleep(2)  # Зачекати 2 секунди, потім скасувати
        cancel_event.set_result(True)
        result = await task
        print(f"Отримано результат: {result}")
    except asyncio.CancelledError:
        print("Роботу скасовано.")

if __name__ == "__main__":
    asyncio.run(main())
