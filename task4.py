import asyncio
import aiofiles

async def generate_large_data(filename="data/large_data.txt", lines=100000):
    """Генерує великий файл даних."""
    async with aiofiles.open(filename, mode="w") as f:
        for i in range(lines):
            await f.write(f"Line {i}\n")

async def main():
    await generate_large_data()
    print("Large data file generated.")

if __name__ == "__main__":
    asyncio.run(main())
