from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
from .models import *
from .forms import *
import urllib.request
from google.cloud import vision
import io
import cv2
import numpy as np
import os
import boto3

# 테스트용
def keyboard(request):
    return JsonResponse({
        'type': 'text',
        'test': 'success'
    })

@csrf_exempt
def recommend(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_act = return_json_str['action']['detailParams']
    symptom = return_act['symptom_name']['value']

    if symptom:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '{}을 겪으시는군요.\n 약과 음식 중 무엇을 추천해드릴까요?'.format(symptom)
                        }
                    }],
                'quickReplies': [{
                    'label': '약품',
                    'action': 'message',
                    'messageText': '{}을 위한 약품'.format(symptom)
                    },
                    {
                    'label': '음식',
                    'action': 'message',
                    'messageText': '{}을 위한 음식'.format(symptom)
                    }]
                }
            })

@csrf_exempt
def medicine(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index('을')
    disease = return_str[:idx]
    manu = '제조사: '
    effect = '효능효과 알아보기'
    usage = '복용법 알아보기'
    precautions = '주의사항 알아보기'

    if return_str == disease + '을 위한 약품':
        disease_id = TBL_DISEASE_INFO.objects.get(disease=disease).id
        can = TBL_MEDICINE_INFO.objects.filter(disease=disease_id)
        return JsonResponse({
                 "version": "2.0",
                 "template": {
                 "outputs": [
                {
                     "carousel": {
                         "type": "basicCard",
                         "items": [
                {
                             "title": can[0].medicine,
                             "description": manu + can[0].manufacturer,
                             "thumbnail": {
                                 "imageUrl": can[0].imgurl
              },
                             "buttons": [
                {
                                 "action": "message",
                                 "label": "효능효과",
                                 "messageText": can[0].medicine + ' ' + effect
                },
                {
                                 "action": "message",
                                 "label": "복용법",
                                 "messageText": can[0].medicine + ' ' + usage
                },
                {
                                 "action": "message",
                                 "label": "주의사항",
                                 "messageText": can[0].medicine + ' ' + precautions
                }
              ]
            },
            {
                             "title": can[1].medicine,
                             "description": manu + can[1].manufacturer,
                             "thumbnail": {
                                 "imageUrl": can[1].imgurl
              },
                             "buttons": [
                {
                                 "action": "message",
                                 "label": "효능효과",
                                 "messageText": can[1].medicine + ' ' + effect
                },
                {
                                 "action": "message",
                                 "label": "복용법",
                                 "messageText": can[1].medicine + ' ' + usage
                },
                {
                                 "action":  "message",
                                 "label": "주의사항",
                                 "messageText": can[1].medicine + ' ' + precautions
                }
              ]
            },
            {
                             "title": can[2].medicine,
                             "description": manu + can[2].manufacturer,
                             "thumbnail": {
                                 "imageUrl": can[2].imgurl
              },
                             "buttons": [
                {
                                 "action": "message",
                                 "label": "효능효과",
                                 "messageText": can[2].medicine + ' ' + effect
                },
                {                "action": "message",
                                 "label": "복용법",
                                 "messageText": can[2].medicine + ' ' + usage
                },
                {
                                 "action":  "message",
                                 "label": "주의사항",
                                 "messageText": can[2].medicine + ' ' + precautions
                }
              ]
            }
          ]
        }
      }
    ]
  }
})


@csrf_exempt
def med_detail(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index(' ')
    medicine = return_str[:idx]
    effect = '효능효과 알아보기'
    usage = '복용법 알아보기'

    if return_str == medicine + ' ' + effect:
        can = TBL_MEDICINE_INFO.objects.get(medicine=medicine)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': can.effect
                        }
                    }]
                }
            })

    elif return_str == medicine + ' ' + usage:
        can = TBL_MEDICINE_INFO.objects.get(medicine=medicine)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': can.usage
                        }
                    }]
                }
            })

@csrf_exempt
def precautions(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index(' ')
    medicine = return_str[:idx]
    precautions = '주의사항 알아보기'

    if return_str == medicine + ' ' + precautions:
        can = TBL_MEDICINE_INFO.objects.get(medicine=medicine)
        return JsonResponse({
            'version': '2.0',
            'data': {
                'precaution': can.precautions,
                'link': can.reference
                    }
            })

@csrf_exempt
def check(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    medicine = return_str
    can = TBL_MEDLIST_INFO.objects.get(medicine=medicine)

    if can:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': can.effect
                    }
                }],
                'quickReplies': [{
                    'label': '복용법',
                    'action': 'message',
                    'messageText': '{}의 복용법'.format(medicine)
                    },
                    {
                    'label': '주의사항',
                    'action': 'message',
                    'messageText': '{}의 주의사항'.format(medicine)
                    }]
            }
        })

    else:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '죄송하지만 해당 약품은 닥터봇이 좀 더 공부해야 할 것 같아요. 인터넷을 검색하거나 약국을 방문해주세요!'
                    }
                }]
            }
        })

@csrf_exempt
def checkusage(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index('의')
    medicine = return_str[:idx]
    usage = '복용법'

    if return_str == medicine + '의 ' + usage:
        can = TBL_MEDLIST_INFO.objects.get(medicine=medicine)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': can.usage
                        }
                    }],
                    'quickReplies': [{
                        'label': '주의사항',
                        'action': 'message',
                        'messageText': '{}의 주의사항'.format(medicine)
                        }]
                }
            })

@csrf_exempt
def checkprecaution(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index('의')
    medicine = return_str[:idx]
    precautions = '주의사항'

    if return_str == medicine + '의 ' + precautions:
        can = TBL_MEDLIST_INFO.objects.get(medicine=medicine)
        return JsonResponse({
            'version': '2.0',
            'data': {
                'precaution': can.precautions,
                'link': can.reference
                }
            })

@csrf_exempt
def showmap(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_act = return_json_str['action']['detailParams']
    location = return_act['location']['value']

    if location:
        return JsonResponse({
            'version': '2.0',
            'data': {
                'location': 'https://m.map.kakao.com/actions/searchView/?q=' + location + '%20약국#!/all/map/place'
                }
            })

@csrf_exempt
def imageupload(request):
    if request.method == 'POST':
        form = TBL_IMG_INFOFORM(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('imagelist')
            except:
                pass
    else:
        form = TBL_IMG_INFOFORM()

    context = {
            'form': form
        }
    return render(request, 'create.html', context)

@csrf_exempt
def imagelist(request):
    image = TBL_IMG_INFO.objects.last()
    return render(request, 'list.html', {'image': image})

#export GOOGLE_APPLICATION_CREDENTIALS="/home/ubuntu/visionAPI-a21221d148d7.json"
@csrf_exempt
def textract(request):
    import opencvdetect as pp
    import test_pre as qq
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"/home/ubuntu/visionAPI-a21221d148d7.json"
    photo = TBL_IMG_INFO.objects.last()
    path = photo.image.path
    pp.read_configs('./config.yml')
    cropped_images = pp.process_image(path)

    result = qq.get_step_compare_image(path)

    message = qq.read_text_from_image(path)
    message = [v for v in message if v]
    textlist = ' '.join(message)

    translate = boto3.client('translate', region_name='ap-northeast-2')
    result = translate.translate_text(Text=textlist,
                                  SourceLanguageCode="auto",
                                  TargetLanguageCode="ko")
    translated = result["TranslatedText"]

    return render(request, 'textract.html', {'textlist': textlist, 'translated': translated})

@csrf_exempt
def food(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    idx = return_str.index('을')
    disease = return_str[:idx]

    if return_str == disease + '을 위한 음식':
        disease_id = TBL_DISEASE_INFO.objects.get(disease=disease).id
        can = TBL_FOOD_INFO.objects.filter(disease=disease_id)[0]
        return JsonResponse({
                 "version": "2.0",
                 "template": {
                 "outputs": [
                    {
                     "carousel": {
                         "type": "basicCard",
                         "items": [
                            {
                             "title": can.food1,
                             "description": "요리법은 아래 버튼을 클릭!",
                             "thumbnail": {
                                 "imageUrl": can.imgurl1
                            },
                             "buttons": [
                                 {
                                     "action": "webLink",
                                     "label": can.food1 + " 요리 알아보기",
                                     "webLinkUrl": can.youtube1
                                     }
                                 ]
                        },
                            {
                             "title": can.food2,
                             "description": "요리법은 아래 버튼을 클릭!",
                             "thumbnail": {
                                 "imageUrl": can.imgurl2
                            },
                             "buttons": [
                                 {
                                     "action": "webLink",
                                     "label": can.food2 + " 요리 알아보기",
                                     "webLinkUrl": can.youtube2
                                     }
                                 ]
                        }
                    ]
                }
            }
          ]
        }
      })

@csrf_exempt
def mapping(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    if return_str == "귀속이 꽉 막힌 듯한 느낌이 들어":
        import numpy as np
        import pandas as pd
        import tensorflow as tf
        from tensorflow.keras.layers import Dense, Input, Dropout, LSTM
        from tensorflow.keras.optimizers import Adam, SGD, RMSprop
        from tensorflow.keras.models import Model
        from tensorflow.keras.callbacks import ModelCheckpoint
        import tensorflow_hub as hub

        import tokenization

        def bert_encode(texts, tokenizer, max_len=40):
            all_tokens = []
            all_masks = []
            all_segments = []

            for text in texts:
                text = tokenizer.tokenize(text)

                text = text[:max_len-2]
                input_sequence = ["[CLS]"] + text + ["[SEP]"]
                pad_len = max_len - len(input_sequence)

                tokens = tokenizer.convert_tokens_to_ids(input_sequence)
                tokens += [0] * pad_len
                pad_masks = [1] * len(input_sequence) + [0] * pad_len
                segment_ids = [0] * max_len

                all_tokens.append(tokens)
                all_masks.append(pad_masks)
                all_segments.append(segment_ids)

            return np.array(all_tokens), np.array(all_masks), np.array(all_segments)

        def build_model(bert_layer, max_len=40):
            input_word_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
            input_mask = Input(shape=(max_len,), dtype=tf.int32, name="input_mask")
            segment_ids = Input(shape=(max_len,), dtype=tf.int32, name="segment_ids")

            _, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
            clf_output = sequence_output[:, 0, :]
            out = Dense(12, activation='softmax')(clf_output)

            model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=out)
            model.compile(Adam(lr=1e-6), loss='categorical_crossentropy', metrics=['acc'])

            return model

        module_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"
        bert_layer = hub.KerasLayer(module_url, trainable=True)

        mapping = {0: '간염', 1: '고막염', 2: '구내염', 3: '다낭성 난소 증후군', 4: '방광염', 5: '비염', 6: '외이도염', 7: '위염', 8: '장염', 9: '중이염', 10: '질염', 11: '축농증'}

        vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
        do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
        tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

        model = build_model(bert_layer, max_len=40)
        model.summary()


        model.load_weights('/home/ubuntu/myvenv/medchat/medchat_app/final_model.h5')

        test = pd.DataFrame([return_str], columns = ['증상'])
        test_input = bert_encode(test['증상'].values, tokenizer, max_len=40)
        pred = model.predict(test_input)
        disease = mapping[np.where(pred[0] == pred[0].max())[0][0]]

        prob = pred[0].max()

        return JsonResponse({
                'version': '2.0',
                'data': {
                    'disease': disease,
                    'prob': prob
                        }
                })
