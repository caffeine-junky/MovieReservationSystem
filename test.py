import httpx
import asyncio


async def main():

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/auth/login")
            response.raise_for_status()
            print(response.json())
    except Exception as e:
        print(f"Error occured: {e}")


if __name__ == "__main__":
    asyncio.run(main())
