import requests
import base64
import qrcode 

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
print()
# https://imgur.com/a/JMSSSOC