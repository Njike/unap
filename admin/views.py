from app import app
from flask import render_template, url_for, request, jsonify, redirect, url_for, make_response, flash, send_from_directory, abort, Markup
from werkzeug.utils import secure_filename
from datetime import datetime

from models.models import *
import os
from wtforms import StringField, BooleanField, FileField, PasswordField, HiddenField, IntegerField, SelectField, SubmitField, TextField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from helpers.imageHandler import imageHandler, allowed_image

from PIL import Image, ImageOps



## NOTE, USERS WITHOUT ADMIN PRIVILAGES ARE NOT ALLOWED TO USE THESE ADMIN ROUTES
## Edit the delete routes to allow GET requests but returns 404 in get but allows POST requests to go through

# admin = Admin(app, index_view=AdminIndexView())
admin = Admin(app, name="sudo")


def _image_formatter(view, context, model, name):
#     return "hello"
    if model.image_url:
        markupstring = f"<a href='{url_for('get_upload', filename=model.image_url)}'>{url_for('get_upload', filename=model.image_url)}</a>"
        return Markup(markupstring)
    else:
        return ""



class ControllerView(ModelView):
    column_formatters = {
        "image_url": _image_formatter
    }
    form_excluded_columns = ("image_url", "nominees", "award")

    # def is_accessible(self):
    #     # if User.query.all()
    #     return User().isAuthenticated() and User().user().super_user
    #     # else:
    #     #     return User().isAuthenticated()

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return abort(404)



class NomineeController(ControllerView):

    form_extra_fields = {
        'image': FileField('Nominee pic',validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    }

    def update_model(self, form, model):
        """
            Update model from the form.

            Returns `True` if operation succeeded.

            Must be implemented in the child class.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        # print("model =============== ", form.amount)
        if form.data and form.validate:
            model.name = form.name.data
            model.country = form.country.data
            model.description = form.description.data
            model.category = form.category.data

            if form.image.data:
                path = imageHandler(form.image.data)
                model.image_url = path

            model.winner = form.winner.data

            self.session.commit()

            return True








    def create_model(self, form):
        """
           Create model from the form.

           Returns the model instance if operation succeeded.

           Must be implemented in the child class.

           :param form:
               Form instance
        """


        if form.data and form.validate:
            model = self.model()
            path = imageHandler(form.image.data)
            model.name = form.name.data
            model.country = form.country.data
            model.description = form.description.data
            model.category = form.category.data
            model.image_url = path
            model.winner = form.winner.data

            self.session.add(model)
            self.session.commit()

            return model

class JudgesController(ControllerView):

    form_extra_fields = {
        'image': FileField('Judge pic',validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    }

    def update_model(self, form, model):
        """
            Update model from the form.

            Returns `True` if operation succeeded.

            Must be implemented in the child class.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        # print("model =============== ", form.amount)
        if form.data and form.validate:
            model.name = form.name.data
            model.description = form.description.data

            if form.image.data:
                path = imageHandler(form.image.data)
                model.image_url = path


            self.session.commit()

            return True

    def create_model(self, form):
        """
           Create model from the form.

           Returns the model instance if operation succeeded.

           Must be implemented in the child class.

           :param form:
               Form instance
        """


        if form.data and form.validate:
            model = self.model()
            path = imageHandler(form.image.data)
            model.name = form.name.data
            model.description = form.description.data
            model.image_url = path

            self.session.add(model)
            self.session.commit()

            return model

class AwardController(ControllerView):

    form_extra_fields = {
        'image': FileField('Award pic',validators=[FileAllowed(['jpg', 'jpeg','png'], 'Images only!')])
    }

    def update_model(self, form, model):
        """
            Update model from the form.

            Returns `True` if operation succeeded.

            Must be implemented in the child class.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        # print("model =============== ", form.amount)
        if form.data and form.validate:
            model.name = form.name.data
            model.show_on_billboard = form.show_on_billboard.data
            model.category = form.category.data
            model.description = form.description.data

            if form.image.data:
                path = imageHandler(form.image.data)
                model.image_url = path


            self.session.commit()

            return True

    def create_model(self, form):
        """
           Create model from the form.

           Returns the model instance if operation succeeded.

           Must be implemented in the child class.

           :param form:
               Form instance
        """


        if form.data and form.validate:
            model = self.model()
            path = imageHandler(form.image.data)
            model.name = form.name.data
            model.show_on_billboard = form.show_on_billboard.data
            model.category = form.category.data
            model.description = form.description.data
            model.image_url = path

            self.session.add(model)
            self.session.commit()

            return model




@app.route("/uploads/<path:filename>")
def get_upload(filename):
    try:
        return send_from_directory(app.config["UPLOADS"], filename=filename, as_attachment=False)
    except:
        abort(404)


admin.add_view(NomineeController(Nominees, db.session))





admin.add_view(ControllerView(AwardCategory, db.session))
admin.add_view(ControllerView(BestJudgeWriteUp, db.session))
admin.add_view(ControllerView(RecentNomineeWriteUp, db.session))
admin.add_view(JudgesController(Judges, db.session))
admin.add_view(AwardController(Awards, db.session))


