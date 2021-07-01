# $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\User\Desktop\visionAPI-a21221d148d7.json"

from google.cloud import vision
import io
import urllib.request


uri = 'https://www.londondrugs.com/on/demandware.static/-/Sites-londondrugs-master/default/dw1114f20b/products/L2710507/large/L2710507.JPG'

client = vision.ImageAnnotatorClient()
image = vision.types.Image()
image.source.image_uri = uri

response = client.text_detection(image=image)
texts = response.text_annotations

textlist = ''
    #print('Texts:')
for text in texts:
    textlist = textlist + text.description
print(textlist)
    #vertices = (['({},{})'.format(vertex.x, vertex.y)
                #for vertex in text.bounding_poly.vertices])

    #print('bounds: {}'.format(','.join(vertices)))

#if response.error.message:
    #raise Exception(
        #'{}\nFor more info on error messages, check: '
        #'https://cloud.google.com/apis/design/errors'.format(
            #response.error.message))
