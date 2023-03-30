import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import time, replicate, urllib.request, os, io, sys, requests, base64, qrcode
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from multiprocessing import Process


#Env Variables: 
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = ''
os.environ["REPLICATE_API_TOKEN"]=""

#API for clip interrogator
model = replicate.models.get("francduartemar/clip")
version = model.versions.get("65b3868d183aeb07df77369443a2b5a2c59288bd03081d62226f96156bc45b5a")

#API DreamStudio
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=False,
    engine="stable-diffusion-512-v2-1",
)

#Camera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration({"size":(3840,2160)})
#camera_config = picam2.create_still_configuration({"size":(5184,3456)})
picam2.configure(camera_config)
picam2.start()
picam2.set_controls({"AfMode": 2,"AfTrigger": 0})
#I/O
BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
prev_state = GPIO.input(BUTTON_PIN)

def blink():
    while True:
        global stop_threads
        GPIO.output(23,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(23,GPIO.LOW)
        time.sleep(5)
        if stop_threads:
            print("Breaking")
            break

GPIO.output(18,GPIO.HIGH)
#Take picture
ACTIVE = True
MAX_SHUT = 1

try:
    while ACTIVE:
        time.sleep(0.01)
        button_state = GPIO.input(BUTTON_PIN)
        if button_state != prev_state:
            if(button_state == GPIO.LOW):
                MAX_SHUT-=1
                # picam2.capture_file("test{x}.jpg".format(x=MAX_SHUT))
                imageCap = picam2.capture_file("picture.png")
                ACTIVE=False
    


except KeyboardInterrupt:
    GPIO.cleanup()
    quit()
picam2.stop()
print("Processing Image")
GPIO.output(18,GPIO.LOW)

stop_threads = False
t1 = Process(target = blink)
t1.start()
time.sleep(0.5)

#AI STUFF
inputs = {
    # Input image
    # 'image': open("path/to/file", "rb"),
    'image':open("picture.png","rb"),

    # Choose ViT-L for Stable Diffusion 1, and ViT-H for Stable Diffusion
    # 2
    'clip_model_name': "ViT-H-14/laion2b_s32b_b79k",

    # Prompt mode (best takes 10-20 seconds, fast takes 1-2 seconds).
    'mode': "fast",
}

# https://replicate.com/francduartemar/clip/versions/65b3868d183aeb07df77369443a2b5a2c59288bd03081d62226f96156bc45b5a#output-schema
outputText = version.predict(**inputs)
print(outputText)

answers = stability_api.generate(
    prompt=outputText,
    steps=75,
    cfg_scale=8.0,
    width=768,
    height=512,
    samples=1,
    sampler=generation.SAMPLER_K_DPMPP_2M
)

for resp in answers:
    for artifact in resp.artifacts:
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.save("Stable.png")
            print("Saved images")

with open("Stable.png", "rb") as stable_image_file:
    stable_encoded_string = base64.b64encode(stable_image_file.read())
    
with open("ogImage.jpg", "rb") as taken_image_file:
    taken_encoded_string = base64.b64encode(taken_image_file.read())

urlImageUpload = "https://api.imgur.com/3/image"
client_id = "cb22489d49f3063"
files=[]
headers = {
  'Authorization': 'Client-ID cb22489d49f3063'
}

responseStable = requests.request("POST", urlImageUpload, headers=headers, data={'image': stable_encoded_string}, files=files)
deltehash1 = responseStable.json()["data"]["deletehash"]

responseTaken = requests.request("POST", urlImageUpload, headers=headers, data={'image': taken_encoded_string}, files=files)
deltehash2 = responseTaken.json()["data"]["deletehash"]

urlAlbum= "https://api.imgur.com/3/album"

payloadAlbum={'deletehashes[]': [deltehash2,deltehash1],
'title': 'PI Cam Images',
'description': 'Raspberry Pi Images',
'cover': 'deltehash1'}
files=[
]

albumResponse = requests.request("POST", urlAlbum, headers=headers, data=payloadAlbum, files=files)
albumID = albumResponse.json()["data"]["id"]
albumLink = "https://imgur.com/a/"+albumID
img = qrcode.make(albumLink)

img.save('MyQRCode1.png')

print("Album Link: ",albumLink)

# urllib.request.urlretrieve(outputStab[0],"Stable.jpg")
stop_threads = True
t1.terminate()
GPIO.cleanup()
print("Finished")
#sys.exit()
