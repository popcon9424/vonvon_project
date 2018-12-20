import requests
from flask import Flask, render_template, request
from faker import Faker
import random
import csv

app = Flask(__name__)
fake = Faker('ko_KR')

# '/' : 사용자의 이름을 입력받습니다.
@app.route("/")
def index():
    return render_template("index.html")
    
log_past = {}
    
@app.route("/past")
def pasttool():
    return render_template("past.html")
    
# '/pastlife' : 사용자의 (랜덤으로 생성된) 전생/직업을 보여준다.
@app.route("/pastlife")
def vonvon():
    name = request.args.get('name')
    job = fake.job()
    value = log_past.get(name,"")
    if value == "":
        log_past[name] = job
    else:
        job = value
    return render_template('pastlife.html', name=name, job=job)
    
log_match = []
log_match_name = []
    
@app.route("/match")
def match():
    return render_template("match.html")
    
@app.route("/match_check")
def match_check():
    # 1. fake 궁합을 알려주고
    # 2. 우리만 알 수 있게 저장한다.
    # - log_match 리스트에 append를 통해 저장한다.
    # 3. match.html 에는 두 사람의 이름과 random으로 생성된
    #    50~100 사이의 수를 함께 보여준다.
    #    ex) XX님과 YY님의 궁합은 00%입니다.
    me = request.args.get('me')
    you = request.args.get('you')
    ind = -1
    for i in range(50,101):
        if [me,you,i] in log_match:
            ind = log_match.index([me,you,i])
    if ind == -1:
        percent = random.choice(range(50,101))
        log_match.append([me,you,percent])
    else:
        percent = log_match[ind][2]
        
    # CSV 파일을 통한 데이터 영구 저장
    # with 구문은 open한 파일을 임시적으로 제어하고
    # 제어가 끝나면 자동으로 close함
    with open('log_match.csv', 'a', encoding="utf-8") as f:
        name_list = csv.writer(f)
        name_list.writerow([me, you])
        
    return render_template('match_check.html', me=me, you=you, percent=percent)

@app.route('/admin')
def admin():
    # 낚인 사람들의 명단
    # - template에서 반복(for)을 써서
    # log_match 에 있는 데이터를 모두 보여준다.
    
    # for i in range(len(log_match)):
    #     log_match_name.append([log_match[i][0],log_match[i][1]])
    
    data = []
    
    with open('log_match.csv', 'r', encoding="utf-8") as f:
        for name in f:
            data.append(name)
                
    return render_template('admin.html', data = data)