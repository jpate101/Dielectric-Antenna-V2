import serial
import time

# Initialize serial port (use the correct port for your system)
serialPort = serial.Serial(port="COM5", baudrate=9600, timeout=1.0, bytesize=serial.EIGHTBITS)

# Give the Arduino some time to initialize
time.sleep(2)

# Clear any previous data in the serial buffer
serialPort.flushInput()

# Send command "4" to check connection
command = "4"  # Command to check connection
print(f"Sending command: {command.strip()}")

# Write the command to Arduino
serialPort.write(command.encode())

# Read the response from Arduino
response = serialPort.readline().decode().strip()  # Read and decode the response

# Debugging: Print out the raw response for troubleshooting
print(f"Raw response: {response}")

if response:
    print(f"Received response: {response}")
else:
    print("No response received")

# Close the serial port
serialPort.close()