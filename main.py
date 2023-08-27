import time
import machine
import urequests
import ssd1306
from collections import deque


print("main.py -- running main code")

# URL of the API endpoint
api_url = "https://api.davidk.tech/api/nations"

# Make an HTTP GET request to the API
#response = urequests.get(api_url)

# Print the response content
#print(response.text)

# Close the response
#response.close()

# Configure the display I2C connection
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))

# Screen
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Led 
led_pin = machine.Pin(2, machine.Pin.OUT)

# Distance measure
trigger_pin = machine.Pin(5, machine.Pin.OUT)
echo_pin = machine.Pin(4, machine.Pin.IN)

# Motor inputs
motor1_direction = machine.Pin(25, machine.Pin.OUT)
motor1_speed = machine.PWM(machine.Pin(26))
motor2_direction = machine.Pin(32, machine.Pin.OUT)
motor2_speed = machine.PWM(machine.Pin(33))

# Set initial motor directions
motor1_direction.value(1)
motor2_direction.value(1)
motor1_speed.duty(0)
motor2_speed.duty(0)

def measure_distance():
    # Trigger the sensor by sending a pulse on the trigger pin
    trigger_pin.on()
    time.sleep_us(10)
    trigger_pin.off()

    # Measure the time it takes for the echo signal to return
    pulse_time = machine.time_pulse_us(echo_pin, True, 1000000)  # 1 second timeout

    # Calculate distance using the speed of sound (343 m/s)
    distance = (pulse_time  * 0.000343) / 2  # Divide by 2 for one-way distance

    # round the distance to 2 decimal places
    distance = round(distance, 2)

    return distance

# Initialize variables for scrolling
text_queue = []

def set_display():
    # Remove old items from the queue to limit its size (adjust as needed)
    if len(text_queue) > 6:
        text_queue.pop(0)

    # Clear the display
    oled.fill(0)

    # Display the text from the queue
    y_position = 0
    for line in text_queue:
        # Display each line of text at a specific y-position
        oled.text(line.strip("\n"), 0, y_position)
        y_position += 10

    # Update the display (replace with your library's display update)
    oled.show()

    # Delay before updating the queue
    time.sleep(0.2)


# Function to drive Motor 1
def drive_motor1(direction, speed):
    motor1_direction.value(direction)
    motor1_speed.duty(speed)

# Function to drive Motor 2
def drive_motor2(direction, speed):
    motor2_direction.value(direction)
    motor2_speed.duty(speed)

def turn_left():
    drive_motor1(direction=0, speed=0)  # Adjust speed as needed
    drive_motor2(direction=0, speed=1000)  # Adjust speed as needed
    time.sleep(0.5)

def turn_right():
    drive_motor1(direction=0, speed=1000)  # Adjust speed as needed
    drive_motor2(direction=0, speed=0)  # Adjust speed as needed
    time.sleep(0.5)

def turn_around():
    drive_motor1(direction=0, speed=1000)  # Adjust speed as needed
    drive_motor2(direction=0, speed=1000)  # Adjust speed as needed
    time.sleep(1.5)

def drive_forward():
    drive_motor1(direction=0, speed=1000)  # Adjust speed as needed
    drive_motor2(direction=0, speed=1000)  # Adjust speed as needed
    time.sleep(0.5)

def drive_backward():
    drive_motor1(direction=1, speed=1000)  # Adjust speed as needed
    drive_motor2(direction=1, speed=1000)  # Adjust speed as needed
    time.sleep(0.5)

def stop():
    drive_motor1(direction=0, speed=0)  # Adjust speed as needed
    drive_motor2(direction=0, speed=0)  # Adjust speed as needed
    time.sleep(0.5)

led_pin.on()
while True:
    distance = measure_distance()
    print("Distance:", distance, "meters")

    if distance > 0.4:
        drive_forward()
    elif distance < 0.4:
        turn_left()

        if distance < 0.1:
            turn_around()

        

    else:
        # Drive both motors forward
        led_pin.off()
        drive_motor1(direction=0, speed=0)  # Adjust speed as needed
        drive_motor2(direction=0, speed=0)  # Adjust speed as needed

    set_display()
    text_queue.append("Dist: " + str(distance) + " m\n")

    drive_motor1(direction=0, speed=0)  # Adjust speed as needed
    drive_motor2(direction=0, speed=0)  # Adjust speed as needed