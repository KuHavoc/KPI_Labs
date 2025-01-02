import asyncio
import aiofiles

async def generate_large_data(filename="data/large_data.txt", lines=100000):
    """Генерує великий файл даних."""
    async with aiofiles.open(filename, mode="w") as f:
        for i in range(lines):
            await f.write(f"Line {i}\n")

async def process_line(line):
    """Обробляє одну лінію даних."""
    await asyncio.sleep(0.001)  # Імітація обробки
    return line.strip().upper()

async def process_large_data(filename="data/large_data.txt"):
    """Читає та обробляє великий файл даних асинхронно."""
    async with aiofiles.open(filename, mode="r") as f:
        async for line in f:
            processed_line = await process_line(line)
            print(f"Processed: {processed_line}")

async def main():
    await generate_large_data()
    print("Large data file generated.")
    await process_large_data()

if __name__ == "__main__":
    asyncio.run(main())
