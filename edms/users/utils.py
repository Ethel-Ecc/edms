import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from edms import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, pic_file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + pic_file_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_filename)
    image_resize = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(image_resize)
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@edms.com',
                  recipients=[user.email],
                  )
    msg.body = f''' To reset your password, use this link\n{url_for('users.reset_password', token=token, _external=True)}\n
If you did not make this request, simply ignore this message and no changes will be made
'''
    mail.send(msg)
