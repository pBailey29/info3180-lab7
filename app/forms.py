# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileAllowed, FileRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[
        DataRequired(message='Movie title is required')
    ])
    
    description = TextAreaField('Description', validators=[
        InputRequired(message='Please provide a brief description of the movie')
    ])
    
    poster = FileField('Movie Poster', validators=[
        FileRequired(message='Please upload a movie poster'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only image files are allowed (jpg, jpeg, png)')
    ])