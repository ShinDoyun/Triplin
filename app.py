from flask import Flask, redirect, url_for, render_template, request, json, flash

app = Flask(__name__)
app.secret_key = 'default value'
database_path = 'static/database/user_info.json'


@app.route('/login', host="test.localhost.com:5000")
def login():
    return render_template('Login.html')


@app.route('/login/try', methods=['POST'])
def try_login():
    return loginChecking(request.form['triplin_id'], request.form['triplin_password'])


@app.route('/', host="test.localhost.com:5000")
def root_page():
    if request.cookies.get('cookie_token'):
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/sign_up')
def signup():
    return '회원가입 페이지'


@app.route('/main')
def main():
    uid = request.cookies.get('cookie_token')
    if str(uid) == 'None':
        return redirect(url_for('login'))

    user_info_data = open(database_path, 'r').read()
    user_info_json = json.loads(user_info_data)
    employee_info = user_info_json['employeesInfo'][uid]

    return_str = "이름 : " + employee_info['name'] + ' 남은 연차 : ' + str(employee_info['annualLeave'])

    return render_template('Main.html', text=return_str)


@app.route('/vacation')
def vacation():
    # 유저 권한에 따라 관리자 or 직원 전용 페이지가 나뉨/Users/shindoyoon/PycharmProjects/VacationManagerSystem/static/jwt.
    return '휴가 페이지'


@app.route('/vacation/employee')
def vacation_employee():
    return '휴가_직원 전용'


@app.route('/vacation/employee/my_page')
def vacation_empoloyee_mypage():
    return '휴가_직원_마이페이지'


@app.route('/vacation.employee/attendance_check')
def vacation_employee_attendance_check():
    return '휴가_직원_출근체크'


@app.route('/vacation/employee/request_vacation')
def vacation_employee_vacation():
    return '휴가_직원_휴가신청'


@app.route('/vacation/manager')
def vacation_manager():
    return '휴가_관리자 전용'


def loginChecking(id, password):
    user_info_data = open(database_path, 'r').read()
    user_info_json = json.loads(user_info_data)

    if id in user_info_json['loginInfo']:
        if user_info_json['loginInfo'][id]['password'] == password:
            resp = redirect(url_for('main'))
            resp.set_cookie('cookie_token', user_info_json['loginInfo'][id]['uid'])
            return resp

    flash('ID or Password is Not Available')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()