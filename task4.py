import asyncio
import aiofiles
from asyncio import Semaphore

async def generate_large_data(filename="data/large_data.txt", lines=100000):
    """Генерує великий файл даних."""
    async with aiofiles.open(filename, mode="w") as f:
        for i in range(lines):
            await f.write(f"Line {i}\n")

async def process_line(line):
    """Обробляє одну лінію даних."""
    await asyncio.sleep(0.001)  # Імітація обробки
    if "500" in line:
        raise ValueError("Error processing line with 500")
    return line.strip().upper()

async def process_large_data(filename="data/large_data.txt", concurrency_limit=10):
    """Читає та обробляє великий файл даних асинхронно з обмеженням на кількість одночасних задач."""
    semaphore = Semaphore(concurrency_limit)
    async with aiofiles.open(filename, mode="r") as f:
        async def process_with_semaphore(line):
            async with semaphore:
                try:
                    return await process_line(line)
                except ValueError as e:
                    print(f"Error processing line: {e}")
                    return None

        tasks = [process_with_semaphore(line) async for line in f]
        for task in asyncio.as_completed(tasks):
            processed_line = await task
            if processed_line:
                print(f"Processed: {processed_line}")

async def main():
    await generate_large_data()
    print("Large data file generated.")
    await process_large_data()

if __name__ == "__main__":
    asyncio.run(main())
