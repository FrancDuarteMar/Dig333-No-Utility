import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import time, replicate, urllib.request, os, io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

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
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()

#I/O
BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)#

GPIO.setup(BUTTON_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
prev_state = GPIO.input(BUTTON_PIN)

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
                imageCap = picam2.capture_file("ogImage.jpg")
                ACTIVE=False


except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()

print("Processing Image")

#AI STUFF
inputs = {
    # Input image
    # 'image': open("path/to/file", "rb"),
    'image':open("ogImage.jpg","rb"),

    # Choose ViT-L for Stable Diffusion 1, and ViT-H for Stable Diffusion
    # 2
    'clip_model_name': "ViT-H-14/laion2b_s32b_b79k",

    # Prompt mode (best takes 10-20 seconds, fast takes 1-2 seconds).
    'mode': "best",
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
            img.save("Stable.png") # Save our generated images with their seed number as the filename.

# urllib.request.urlretrieve(outputStab[0],"Stable.jpg")

