from machine import ADC, Pin
from servo import PositionServo
from mysecrets import adafruitKey,buttoncode
from airtablesecrets import BASE_ID, API_KEY, TABLE_ID, RECORD_ID
import time, math, random, gamepad, mqtt, connectWifi, requests, asyncio

thermistor = ADC(0)
myservo = PositionServo(16)
LED = Pin(0, Pin.OUT)
print('Initializing Servo...')

myservo.set_position(180)
time.sleep(1)
myservo.set_position(0)
time.sleep(1)
myservo.set_position(90)
pad = True
LED.off()
color = ('None', '#000000')
Temps= {
    'TempC': None,
    'TempF': None,
}
temp = [False]
unit = 'F'
colorname = ['None']
servomode = 'Fake'
buttonseq = []

username = 'Cjt516'
key = adafruitKey

endpoint = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/recibgkdJNi2iuE3P'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

try:
    mygamepad = gamepad.Gamepad(1, scl_pin=19, sda_pin=18)
    print('Connected to Gamepad...')
except OSError:
    print('Gamepad Error')
    pad = False
    pass


def MQTTConnect():
    try:
        global client
        client = mqtt.MQTTClient('NewChrisPico', server='io.adafruit.com', user=username, password=key, ssl=False)
        client.connect()
        print('Connected to MQTT Broker')
    except OSError as e:
        print('Failed')


def setServo(temp):
    temp = int(temp)
    pos = 3 * temp - 90
    if pos > 180:
        pos = 180
    elif pos < 0:
        pos = 0
    myservo.set_position(pos)


def getTempSH(Vout):
    # Steinhart Constants
    A = .4775438117e-3
    B = 3.362081803e-4
    C = -2.539410413e-7
    
    
    #Get Resistance
    Rt = (Vout * 10000) / (3.3 - Vout)
    #print(Rt)
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15
    
    TempF = TempC*(9/5)+32

    return TempC,TempF


def getTempBeta(Vout):
    # Constants for the Beta value calculation
    R0 = 10000  # Resistance at 25°C
    Beta = 3380  # Beta value
    T0 = 25  # Reference temperature in Celsius

    Rt = (10000*Vout)/(3.3 - Vout)
    
    TempC = 1 / (1 / (T0 + 273.15) + (1 / Beta) * math.log(Rt / R0))-273.15
    
    TempF = TempC*(9/5)+32
    
    return TempC,TempF


MQTTConnect()


async def update_temperature(Temps,temp):
    while True:
        adcval = thermistor.read_u16() * (3.3 / 65535)
        TempC, TempF = getTempBeta(adcval)
        #setServo(TempF)
        
        # Store the temperature values in the dictionary
        Temps['TempC'] = TempC
        Temps['TempF'] = TempF
        print(Temps,temp)
        temp[0] = True
        await asyncio.sleep(10)  # Update temperature every 30 seconds

async def update_adafruit(Temps, unit, colorname, client, color,temp):
    last_color = None  # Keep track of the last color to detect changes

    while True:
        if colorname[0] == 'Red':
            unit = 'F'
            new_color = ('Red', '#FF0000')
        elif colorname[0] == 'Green':
            unit = 'C'
            new_color = ('Green', '#00BF00')
        elif colorname[0] == 'None':
            new_color = ('None', '#000000')
        else:
            new_color = color  # Use the previous color if colorname is not recognized

        if new_color != last_color:  # Check if the color has changed
            stringsend = f"{Temps['TempF']:.1f} Degrees F" if unit == 'F' else f"{Temps['TempC']:.2f} Degrees C"
            client.publish('Cjt516/feeds/temperature', stringsend)
            client.publish('Cjt516/feeds/color', str(new_color[1]))
            client.publish('Cjt516/feeds/angry', str(new_color[0]))
            last_color = new_color  # Update last_color
        elif temp[0]:
            stringsend = f"{Temps['TempF']:.1f} Degrees F" if unit == 'F' else f"{Temps['TempC']:.2f} Degrees C"
            client.publish('Cjt516/feeds/temperature', stringsend)
            client.publish('Cjt516/feeds/color', str(new_color[1]))
            client.publish('Cjt516/feeds/angry', str(new_color[0]))
            temp[0] = False

        await asyncio.sleep(1)  # Update Adafruit every 1 second


async def pull_airtable(colorname):
    while True:
        response = requests.get(endpoint, headers=headers)
        colorname[0] = response.json()['fields']['Color Name']
        #print('Actual colorname:',colorname)
        await asyncio.sleep(1)  # Pull from Airtable as fast as possible


async def check_gamepad(Temps,buttonseq,servomode):
    while True:
        if pad == True:
            buttons = mygamepad.readbuttons()
            if buttons != [False, False, False, False, False, False]:
                if servomode == 'Fake':
                    buttonseq.append(buttons)
                    LED.off()
                    time.sleep(.1)
                    LED.on()
                else:
                    if buttons == 'start':
                        servomode = 'Fake'
            if buttons == 'start':
                buttonseq.clear()
            if buttonseq == buttoncode:
                servomode = 'Real'
                buttonseq.clear()
            if servomode == 'Real':
                setServo(Temps['TempF'])
            else:
                setServo(random.randint(30,90))
            #print(buttonseq)
        else:
            setServo(Temps['TempF'])
        await asyncio.sleep(.1)  # Check gamepad as fast as possible
        
LED.on()
try:
    loop = asyncio.get_event_loop()
    loop.create_task(update_temperature(Temps,temp))
    loop.create_task(pull_airtable(colorname))
    loop.create_task(update_adafruit(Temps,unit,colorname,client,color,temp))
    loop.create_task(check_gamepad(Temps,buttonseq,servomode))
    loop.run_forever()
except KeyboardInterrupt:
    LED.off()
