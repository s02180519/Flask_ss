import json

from app.admin import bluePrint
from app.admin.forms import RegisterForm, RegisterUsers
from app.models import User, Group, Group_user
from app import dataBase
# from werkzeug.local import LocalProxy
from flask import render_template, flash, redirect, url_for, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from distutils.dir_util import copy_tree
import random
from datetime import date
import string
import os
import shutil
from sqlalchemy import desc


def checkGroup():
    # current_user.username
    # users = Group_user.query.join(User, User.id == Group_user.userid).filter(Group_user.groupid == 2)
    # users = Group_user.query.select_from(User).join(Group_user, User.id == Group_user.userid).filter(User.username == current_user.username)
    adminId = Group.query.filter(Group.groupname == 'admin').first()
    user = Group_user.query.select_from(User).join(Group_user, User.id == Group_user.userid).filter(User.username == current_user.username).filter(Group_user.groupid == adminId.id).first()
    if user is None:
        return False
    else:
        return True
    # if current_user.username != 'ucmc2020ssRoot':
    #     return False
    # else:
    #     return True


@bluePrint.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    # if current_user.username != 'ucmc2020ssRoot':

    if checkGroup() is False:
        return render_template('errors/500.html')
    if request.method == 'POST':
        data = request.get_json()
        for userName in data['usersDelete']:
            User.query.filter_by(username=userName).delete(synchronize_session=False)
            usr_folder = 'userdata/' + userName
            if os.path.exists(usr_folder):
                # path = os.path.join(os.path.abspath(usr_folder), 'TestDir')
                shutil.rmtree(usr_folder)
                # os.rmtree(usr_folder)
        dataBase.session.commit()
        # data = {"some_key": "some_value"}  # Your data in JSON-serializable type
        # response = app.response_class(response=json.dumps(data),
        #                               status=200,
        #                               mimetype='application/json')
        # return response
        return json.dumps({'status': 'OK'})
    # выбираем пользователей по дате последней авторизации (по убыванию)
    arUsers = User.query.order_by(desc(User.last_seen))
    # for user in arUsers:
    # return render_template('admin/users.html', title='Пользователи', arUsers=arUsers, arUsersLen=len(arUsers))
    return render_template('admin/users.html', title='Пользователи', arUsers=arUsers)


# переадресация на страницу регистрации новых пользователей
@bluePrint.route('/admin')
@login_required
def admin_forward():
    # if current_user.username != 'ucmc2020ssRoot':
    #     return render_template('errors/500.html')
    if checkGroup() is False:
        return render_template('errors/500.html')

    form = RegisterUsers()
    return render_template('admin/register.html', title='Регистрация', form=form, arUsers=[], arUsersLen=0)


# страница регистрации новых пользователей
@bluePrint.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin():
    # print(current_user.username)
    # if current_user.username != 'ucmc2020ssRoot':
    #     return render_template('errors/500.html')
    if checkGroup() is False:
        return render_template('errors/500.html')
    # current_user = LocalProxy(lambda: _get_user())
    form = RegisterUsers()
    # Отправили заполненную форму
    if form.validate_on_submit():
        arUsers = []
        new_user_count = int(form.userNumber.data)
        current_users_count = 0
        year = date.today().strftime('%Y')
        # поиск номера несуществуюего пользователя
        while 1:
            curUser = 'ucmc' + year + 'ss' + format(current_users_count, '03d')
            user = User.query.filter_by(
                username=curUser).first()
            if user is None:
                break
            current_users_count += 1
        # добавление новых пользователей
        for i in range(0, new_user_count):
            usr_name = 'ucmc' + year + 'ss' + format(i + current_users_count, '03d')
            txt_pass_count = 12
            usr_list = open("User_list.txt", "a")
            txt_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=txt_pass_count))
            usr_list.write(usr_name + " : " + txt_pass + "\n")
            # It works correctly but further investigation on what's going on required.
            new_user = User(username=usr_name, local_folder=usr_name)
            new_user.set_password(txt_pass)
            dataBase.session.add(new_user)
            # create folders for new users
            usr_folder = 'userdata/' + usr_name
            if not os.path.exists(usr_folder):
                os.makedirs(usr_folder)
            copy_tree('userdata/ucmc2020ssRoot', usr_folder)
            arUsers.append({'login': usr_name, 'password': txt_pass})

        dataBase.session.commit()
        # next_page = request.args.get('next')
        return render_template('admin/register.html', title='Регистрация', form=form, arUsers=arUsers,
                               arUsersLen=len(arUsers))
    return render_template('admin/register.html', title='Регистрация', form=form, arUsers=[], arUsersLen=0)
    # return render_template('admin.html', title='Администрирование')
