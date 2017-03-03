import os

from flask import Flask, jsonify, request, abort 

LIGHT_IDS = ['7', '6', '5', '4', '1']
LIGHT_IDS = ['1', '4', '5', '6', '7']
LIGHT_BRIGHTS = [0, 0, 0, 0, 0]
MAX_BRIGHTNESS = 200
MIN_BRIGHTNESS = 0
NUM_LIGHTS = 5

app = Flask(__name__) 

def set_light(light_id, brightness):
    LIGHT_BRIGHTS[light_id] = brightness
    os.system("echo " + LIGHT_IDS[light_id] + "=" + str(brightness)
              + " > /dev/servoblaster")
    
def blink_light():
    light_id_arg = request.args.get('light_id')

    if not light_id_arg:
        abort(400)

    light_id = int(light_id_arg)
        
    if light_id < 0 or light_id >= 5:
        abort(400)

    brightness = MAX_BRIGHTNESS
    while brightness >= MIN_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness -= 2

    while brightness <= MAX_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness += 2

def wave_lights():
    count_downs = [0, 40, 80, 120, 160]
    turning_up = [False, False, False, False, False]   

    for i in range(5):
        set_light(i, MAX_BRIGHTNESS)
        
    set_light(1, MAX_BRIGHTNESS)

    while True:
        for i in range(5):
            if count_downs[i] == 0:
                if not turning_up[i]:
                    set_light(i, LIGHT_BRIGHTS[i] - 1)
                    if (LIGHT_BRIGHTS[i] <= 0):
                        turning_up[i] = True
                else:
                    if (LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS):
                        set_light(i, LIGHT_BRIGHTS[i] + 1)
            else:
                count_downs[i] -= 1

        # this is the worst code I've written all year
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS:
                done = False
        if done:
            return
    
@app.route('/wave')
def wave_endpoint():
    wave_lights()
    return '{}'
    
@app.route('/set_light')
def set_light_endpoint():
    light_id_arg = request.args.get('light_id')
    brightness_arg = request.args.get('brightness')
    
    if not light_id_arg or not brightness_arg:
        abort(400)

    light_id = int(light_id_arg)
    brightness = int(brightness_arg)

    if light_id < 0 or light_id >= 5:
        abort(400)

    if brightness < MIN_BRIGHTNESS or brightness > MAX_BRIGHTNESS:
        abort(400)
        
    set_light(light_id, brightness)
        
    return '{}'

if __name__ == '__main__':
    for i in range(0, NUM_LIGHTS):
        set_light(i, MAX_BRIGHTNESS)
 
    app.run(debug=True)
