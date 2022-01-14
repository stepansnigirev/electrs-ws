#!/usr/bin/env python
import asyncio
import websockets

# blockstream.info:
ELECTRS_IP = "35.201.74.156"
ELECTRS_PORT = 195 # 143 - Testnet, 110 - Mainnet, 195 - Liquid

# reader coro
async def forward(reader, websocket):
    while True:
        data = await reader.readline()
        data = data.strip().decode()
        if data:
            await websocket.send(data)

# keep alive coro
async def ping(writer):
    while True:
        print("ping")
        writer.write(b'{"jsonrpc": "2.0", "method": "server.ping", "params": [], "id": 99999999999}\n')
        await writer.drain()
        await asyncio.sleep(20)

async def echo(websocket):
    reader, writer = await asyncio.open_connection(ELECTRS_IP, ELECTRS_PORT)
    asyncio.create_task(forward(reader, websocket))
    asyncio.create_task(ping(writer))
    async for message in websocket:
        writer.write(message.encode()+b"\n")
        await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    async with websockets.serve(echo, "localhost", 8081):
        await asyncio.Future()  # run forever

asyncio.run(main())
