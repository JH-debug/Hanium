import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input, Dropout, LSTM
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow_hub as hub

import tokenization

def return_answer(userSymptom):
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

    test = pd.DataFrame([userSymptom], columns = ['증상'])
    test_input = bert_encode(test['증상'].values, tokenizer, max_len=40)
    pred = model.predict(test_input)
    disease = mapping[np.where(pred[0] == pred[0].max())[0][0]]

    prob = pred[0].max()
    return disease + str(prob)
#def main():
    #disease

#if__name__ == "__main__":
   # main()
#print(prob)
