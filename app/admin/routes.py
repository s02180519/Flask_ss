from app.admin import bluePrint
from app.admin.forms import RegisterForm, RegisterUsers
from app.models import User
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


@bluePrint.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin():
    print(current_user.username)
    if current_user.username != 'ucmc2020ssRoot':
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
        next_page = request.args.get('next')
        return render_template('admin/register.html', title='Регистрация', form=form, arUsers=arUsers,
                               arUsersLen=len(arUsers))
    return render_template('admin/register.html', title='Регистрация', form=form, arUsers=[], arUsersLen=0)
    # return render_template('admin.html', title='Администрирование')


@bluePrint.route('/register', methods=['GET', 'POST'])
def register_usr():
    form = RegisterForm()
    # Отправили заполненную форму
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            new_user = User(username=form.username.data, local_folder=form.username.data)
            new_user.set_password(form.password.data)
            dataBase.session.add(new_user)
            next_page = request.args.get('next')
            dataBase.session.commit()
            new_usrs = User.query.all()
            print(new_usrs)
            if not next_page or url_parse(next_page).netloc != '':
                return redirect(url_for('auth.login_usr'))
            return redirect(next_page)
        else:
            flash('User login already exists')
            return redirect(url_for('admin.register_usr'))
    return render_template('admin/register.html', title='Регистрация', form=form)
