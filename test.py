import asyncio
import serial


async def read_from_serial(serial_port):
    while True:
        data = await serial_port.read(100)  # Adjust the read size according to your requirements
        if data:
            print(f"Received: {data.decode()}")


async def write_to_serial(serial_port):
    while True:
        message = input("Enter message to send: ")
        serial_port.write(message.encode())


async def main():
    serial_port = serial.Serial('COM6', baudrate=115200)
    reader_task = asyncio.create_task(read_from_serial(serial_port))
    #writer_task = asyncio.create_task(write_to_serial(serial_port))
    await asyncio.gather(reader_task)


asyncio.run(main())
