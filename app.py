from flask import Flask, jsonify, request, send_file, render_template, url_for
from conn import Postgresql
from datetime import datetime
import pandas as pd
import re
import psycopg2
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import io
from io import BytesIO
from werkzeug.utils import secure_filename
from PIL import Image
import json
# import base64



app = Flask(__name__)

# 질문 챗봇 설정
authenticator = IAMAuthenticator('__QKtihq_-JopuuCyyGFOobLg5hstGny5ox3NRZcJGjU')
assistant = AssistantV2(
    version='2019-02-28',
    authenticator=authenticator)

assistant.set_service_url('https://api.kr-seo.assistant.watson.cloud.ibm.com')


@app.route("/test")
def hello():
    return render_template('test.html', title = 'hello jinja') #view 화면.


# 아이디 중복 확인
@app.route("/check_user_id", methods = ['GET'])
def check_user_id():
    data = request.json
    user_id = data['user_id']

    con = Postgresql()
    query = """SELECT * FROM "user" WHERE user_id = '{}'""".format(user_id)
    con.cursor.execute(query)
    query_result = con.cursor.fetchall()

    if (query_result):
        result = {'result': '아이디 중복', 'message': '아이디가 중복되었습니다. 다른 아이디를 입력해주세요.'}
    else:
        result = {'result': '아이디 생성 가능', 'message': '해당 아이디로 회원가입 가능합니다.'}

    con.close()
    return jsonify(result)


# 회원가입
@app.route("/register", methods = ['POST'])
def register():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']
    user_name = data['user_name']
    user_password = data['user_password']
    now = datetime.now()
    create_date = now.strftime('%Y-%m-%d')

    query = """INSERT INTO "user"(user_id, user_name, user_password, create_date) VALUES('{}', '{}', '{}', '{}')""".format(user_id, user_name, user_password, create_date)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '성공'})


#  로그인
@app.route("/login", methods = ['POST'])
def login():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']
    user_password = data['user_password']

    query = """SELECT * FROM "user" WHERE user_id = '{}' AND user_password =  '{}'""".format(user_id, user_password)
    con.cursor.execute(query)
    query_result = con.cursor.fetchall()

    if (query_result):
        result = {'result': '로그인 성공'}
    else:
        result = {'result': '로그인 실패'}

    con.close()
    return jsonify(result)


# 신조어 추천 단어 리스트 확인
@app.route("/new_word", methods = ['GET', 'POST'])
def new_word():
    con = Postgresql()
    data = request.json
    word_date = data['word_date']

    query = """select word, word_meaning from new_word where word_date = '{}' order by random() limit 5""".format(word_date)
    data = pd.read_sql(query, con = con.db)
    # data.values.tolist()
    # {"word": data['word'].values.tolist(), "word_meaning": data['word_meaning'].values.tolist()}
    con.close()
    return jsonify(data.to_dict(orient = 'records'))


# 게시판 글 쓰기
@app.route("/board_write", methods = ['GET', 'POST'])
def board_write():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']
    content = data['content']
    user_name = data['user_name']
    now = datetime.now()
    write_date = now.strftime('%Y-%m-%d')
    good_count = 0
    comment_number = 0

    query_1 = """select board_id from board order by board_id desc limit 1"""
    con.cursor.execute(query_1)
    query_result = con.cursor.fetchall()
    query_result = "".join(str(query_result))
    number = int(re.findall('\d+', query_result)[0])
    board_id = 'b' + str(number + 1)


    query_2 = """INSERT INTO "board"(board_id, user_id, user_name, good_count, content, write_date, comment_number) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(board_id, user_id, user_name, good_count,content, write_date, comment_number)
    con.cursor.execute(query_2)
    con.db.commit()
    con.close()
    return jsonify({'result': '글 등록 완료'})


# 게시판 글 수정
@app.route("/board_rewrite", methods = ['GET', 'POST'])
def board_rewrite():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']
    content = data['content']
    now = datetime.now()
    write_date = now.strftime('%Y-%m-%d')

    query = """update board set content = '{}',  write_date = '{}' WHERE board_id = '{}'""".format(content, write_date, board_id)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '글 수정 완료'})


# 게시판 글 좋아요 +1
@app.route("/board_like", methods = ['GET', 'POST'])
def board_like():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']

    query_1 = """SELECT good_count FROM "board" WHERE board_id = '{}'""".format(board_id)
    con.cursor.execute(query_1)
    query_result = con.cursor.fetchall()
    query_result = "".join(str(query_result))
    number = int(re.findall('\d+', query_result)[0])
    good_count = number + 1

    query_2 = """update board set good_count = '{}' WHERE board_id = '{}'""".format(good_count, board_id)
    con.cursor.execute(query_2)
    con.db.commit()
    con.close()
    return jsonify({'result': '글 좋아요 완료'})


# 게시판 댓글 쓰기
@app.route("/comment_write", methods = ['GET', 'POST'])
def comment_write():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']
    user_id = data['user_id']
    user_name = data['user_name']
    comment = data['comment']
    now = datetime.now()
    write_date = now.strftime('%Y-%m-%d')

    query_1 = """select comment_number from board WHERE board_id = '{}'""".format(board_id)
    con.cursor.execute(query_1)
    query_result = con.cursor.fetchall()
    query_result = "".join(str(query_result))
    number = int(re.findall('\d+', query_result)[0])
    comment_number = number + 1

    query_2 = """update board set comment_number = '{}'""".format(comment_number)
    con.cursor.execute(query_2)
    con.db.commit()

    query_3 = """INSERT INTO "comment"(board_id, user_id, comment, write_date, user_name) VALUES('{}', '{}', '{}', '{}', '{}')""".format(board_id, user_id, comment, write_date, user_name)
    con.cursor.execute(query_3)
    con.db.commit()
    con.close()
    return jsonify({'result': '댓글 등록 완료'})


# 게시판 댓글 수정
@app.route("/comment_rewrite", methods = ['GET', 'POST'])
def comment_rewrite():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']
    user_id = data['user_id']
    comment = data['comment']
    now = datetime.now()
    write_date = now.strftime('%Y-%m-%d')

    query = """update comment set comment = '{}',  write_date = '{}' WHERE board_id = '{}' and user_id = '{}'""".format(comment, write_date, board_id, user_id)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '댓글 수정 완료'})


# 게시판 글 삭제
@app.route("/board_delete", methods = ['GET', 'POST'])
def board_delete():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']

    query = """delete from "board" where user_id = '{}'""".format(user_id)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '글 삭제 완료'})


# 게시판 댓글 삭제
@app.route("/comment_delete", methods = ['GET', 'POST'])
def comment_delete():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']
    user_id = data['user_id']
    comment = data['comment']

    query = """delete from "comment" where board_id = '{}' and user_id = '{}' and comment = '{}'""".format(board_id, user_id, comment)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '댓글 삭제 완료'})



# 게시판 데이터 전체 보기
@app.route("/board", methods = ['POST', 'GET'])
def board():
    con = Postgresql()
    query = """select * from board"""
    data = pd.read_sql(query, con = con.db)
    con.close()
    return jsonify(data.to_dict(orient = 'records'))



# 게시판 별 댓글 전체 보기
@app.route("/comment", methods = ['POST', 'GET'])
def comment():
    con = Postgresql()
    data = request.json
    board_id = data['board_id']

    query = """select * from "comment" where board_id = '{}'""".format(board_id)
    data = pd.read_sql(query, con = con.db)
    con.close()
    return jsonify(data.to_dict(orient = 'records'))



# 이미지 파일 확장자 확인 함수
def allowed_file(filename):
	ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "svg"]
	return '.' in filename and \
		(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS


# 프로필 이미지 등록
@app.route("/upload_image", methods = ['GET', 'POST'])
def upload_image():
    con = Postgresql()
    data = request.files
    f = data['image']
    MAX_FILE_SIZE = 4 * 1024 * 1024

    if f and allowed_file(f.filename):

        # determine the file size
        blob = f.read()
        file_size = len(blob)

        if file_size > MAX_FILE_SIZE:
            return jsonify(errors=["Exceeded max file size ( 4MB )"]), 413

        file_name = secure_filename(f.filename[:-4])

        # write string ( blob ) to a buffer
        buff = BytesIO()
        buff.write(blob)

        # seek back to the beginning so the whole thing will be read by PIL
        buff.seek(0)

        # read the image
        img = Image.open(buff)

        # Get image data
        (im_width, im_height) = img.size

        # set scale factor
        scale = 200.0 / min(im_width, im_height)

        # resize the image
        img = img.resize((int(scale * im_width), int(scale * im_height)), Image.ANTIALIAS)

        # get new dimensions
        (im_width, im_height) = img.size

        # get center
        xshift = int(max((im_width - 200) / 2, 0))
        yshift = int(max((im_height - 200) / 2, 0))

        # crop the image
        img = img.crop((0 + xshift, 0 + yshift, 200 + xshift, 200 + yshift))

        # store image in memory
        new_iobody = io.BytesIO()
        img = img.convert("RGB")
        img.save(new_iobody, 'JPEG')

        # get the filedata for writing
        filedata = psycopg2.Binary(new_iobody.getvalue())
        print(filedata)

        query = """UPDATE "user" SET image = '' WHERE user_id = ''""".format(filedata, file_name)
        con.cursor.execute(query)
        con.db.commit()
        con.close()
        return jsonify({'result': '이미지 등록 완료'})


# 프로필 (이미지) 보기
@app.route("/profile", methods = ['POST', 'GET'])
def profile():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']

    query = """select image from "user" where user_id = '{}'""".format(user_id)
    con.cursor.execute(query)
    image = con.cursor.fetchall()

    if image:
        return send_file(io.BytesIO(image["image"]),
                         attachment_filename = user_id + '.jpg')

'''
    with open(binary_image) as f:
        image = f.read()

    con.close()
    # return jsonify(data.to_dict(orient = 'records'))
    return jsonify(image)
'''


# 퀴즈 문제 전달하기
@app.route("/quiz", methods = ['GET', 'POST'])
def quiz():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']
    now = datetime.now()
    q_date = now.strftime('%Y-%m-%d')

    query_1 = """SELECT * FROM "quiz_user" WHERE user_id = '{}' and q_date = '{}'""".format(user_id, q_date)
    con.cursor.execute(query_1)
    query_result = con.cursor.fetchall()

    if (query_result):
        result = {'result': '이미 오늘의 퀴즈를 다 푸셨습니다.'}
        con.close()
        return jsonify(result)

    else:
        query_2 = """select * from quiz order by random() limit 1"""
        data = pd.read_sql(query_2, con=con.db)
        con.close()
        return jsonify(data.to_dict(orient='records'))



# 점수 db에 저장하기
@app.route("/save_score", methods = ['GET', 'POST'])
def save_score():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']
    score = data['score']
    now = datetime.now()
    q_date = now.strftime('%Y-%m-%d')

    query = """INSERT INTO "quiz_user"(user_id, score, q_date) VALUES('{}', '{}', '{}')""".format(user_id, score, q_date)
    con.cursor.execute(query)
    con.db.commit()
    con.close()
    return jsonify({'result': '점수 등록 완료'})



# 최근 퀴즈 내역: 점수 전달하기
@app.route("/show_score", methods = ['GET', 'POST'])
def show_score():
    con = Postgresql()
    data = request.json
    user_id = data['user_id']

    query = """SELECT q_date, score FROM "quiz_user" WHERE user_id = '{}'""".format(user_id)
    data = pd.read_sql(query, con=con.db)
    con.close()
    return jsonify(data.to_dict(orient='records'))



# Sessions 생성 - 질문 챗봇 방 개설
@app.route("/start_question", methods = ['GET', 'POST'])
def start_question():
    assistant_id = '4f98009d-9878-4aa7-a115-dff718d05e4c'  # 고정 id
    session_id = assistant.create_session(assistant_id = assistant_id).get_result()['session_id']  # 방 id
    return jsonify({"assistant_id" : assistant_id,
                    "session_id" : session_id})


# 질문 챗봇 방 대화
@app.route("/question", methods = ['GET', 'POST'])
def question():
    
    data = request.json
    assistant_id = data['assistant_id']
    session_id = data['session_id']
    message_input = data['message_input']

    response = assistant.message(assistant_id,
                                 session_id,
                                 input={'text': message_input , 'options':{'return_context': True} },
                                 context = {'metadata' : { 'deployment' : 'myDeployment'}}).get_result()

    # len_output = len(response['output']['generic'])

    messages = []

    if response['output']['generic']:
        for i in response['output']['generic']:
            if i['response_type'] == 'text':
                messages.append(dict(text=i['text']))

            elif i['response_type'] == 'image':
                messages.append(dict(attachment = dict(type = 'image',
                                payload = dict(url = i['source']))))

            elif i['response_type'] == 'option':
                buttons = []
                for b in range(i['options']['lenght']-1):
                    buttons.append(dict(type = 'show_block',
                                        block_names = ['Options'],
                                        title = i['options'][b]['label']))
                    messages.append(dict(attachment = dict(type='template',
                                    payload = dict(template_type='button',
                                    text = i['options']['title'], buttons = buttons))))

    response = dict(output = messages, resultCode = 200, input = message_input)
    print(json.dumps(response, indent=4))
    return jsonify(response)


# Sessions 종료 - 질문 챗봇 방 종료
@app.route("/end_question", methods = ['GET', 'POST'])
def end_question():
    data = request.json
    assistant_id = data['assistant_id']
    session_id = data['session_id']
    assistant.delete_session(assistant_id, session_id).get_result()
    return jsonify({'result': '질문 챗봇 세션 종료'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


'''
if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug = True)
'''