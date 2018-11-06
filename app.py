from flask import Flask, redirect, url_for, render_template, request, json, flash, session
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'EkNd!&e&Qk%Cj7du'
user_info_db_path = '/Users/shindoyoon/PycharmProjects/VacationManagerSystem/static/database/user_info_data'


@app.route('/login')
def login():
    return render_template('Login.html')


@app.route('/login/try', methods=['POST'])
def try_login():
    return login_checking(request.form['triplin_id'], request.form['triplin_password'], request.form.get('auto_login'))


@app.route('/')
def root_page():
    if request.cookies.get('cookie_token'):
        session['uid'] = request.cookies.get('cookie_token')

    if session.get('uid'):
        return redirect(url_for('main'))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    resp = redirect(url_for('login'))
    session.pop('uid', None)
    resp.set_cookie('cookie_token', expires=0)
    return resp


@app.route('/main')
def main():
    if not session.get('uid'):
        return redirect(url_for('login'))

    user_info_db = sqlite3.connect(user_info_db_path).cursor()
    user_info_db.execute("SELECT * FROM employees_info WHERE uid='{}'".format(session['uid']))
    user_info_data = user_info_db.fetchall()

    return render_template('Main.html', uid=user_info_data[0][0], name=user_info_data[0][1], nick_name=user_info_data[0][2],
                           gender=user_info_data[0][3], birth=user_info_data[0][4], phone_number=user_info_data[0][5],
                           second_contacts=user_info_data[0][6], join_day=user_info_data[0][7], address=user_info_data[0][8]
                           )


@app.route('/vacation')
def vacation():
    return render_template('RequestVacationTest.html')


@app.route('/vacation/request', methods=['POST'])
def vacation_request():
    request_vacation(request.form['date'], request.form['period'], request.form['reason'], request.form['type'])
    return redirect(url_for('vacation_mypage'))


@app.route('/vacation/my_page')
def vacation_mypage():
    user_info_db = sqlite3.connect(user_info_db_path).cursor()
    user_info_db.execute("SELECT * FROM vacation_list WHERE uid='{}' ORDER BY DATE(vacation_date) ASC LIMIT 10".format(session['uid']))
    vacation_list_data = user_info_db.fetchall()
    user_info_db.execute("SELECT name FROM employees_info WHERE uid='{}'".format(session['uid']))
    name = user_info_db.fetchall()
    return render_template('MyVacationInfo.html', tuples=vacation_list_data, name=name)


@app.route('/vacation/management')
def vacation_manager():
    return '휴가_관리자 전용'


def login_checking(id, password, auto_login):
    login_info_db = sqlite3.connect(user_info_db_path).cursor()
    login_info_db.execute("SELECT * FROM user_login_info WHERE id='{}' AND password='{}'".format(id, password))
    login_info_data = login_info_db.fetchall()

    if len(login_info_data) == 1:
        session['uid'] = login_info_data[0][0]
        resp = redirect(url_for('main'))
        if auto_login:
            resp.set_cookie('cookie_token', session['uid'])
        return resp
    elif len(login_info_data) >= 2:
        flash("IT'S DATABASE ERROR!!!! PLEASE CALL TORRES !!")
    else:
        flash('ID or Password is Not Available')
    return redirect(url_for('login'))


def request_vacation(date, period, reason, type):
    user_info_db = sqlite3.connect(user_info_db_path)
    user_info_db.cursor().execute("INSERT INTO vacation_list VALUES('{}', '{}', '{}', '{}', '{}', {})".
                                  format(session['uid'], date, reason, time.strftime('%c'), type, period))
    user_info_db.commit()

if __name__ == '__main__':
    app.run()
