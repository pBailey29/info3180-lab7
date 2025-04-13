"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from werkzeug.utils import secure_filename
from flask import render_template, request, jsonify, send_file, current_app
from app.forms import MovieForm
from app.models import Movie
from app import db


def init_routes(app):
    """Register all routes with the app"""

    @app.route('/')
    def index():
        return jsonify(message="This is the beginning of our API")

    @app.route('/<file_name>.txt')
    def send_text_file(file_name):
        file_dot_text = file_name + '.txt'
        return app.send_static_file(file_dot_text)

    @app.after_request
    def add_header(response):
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404


    @app.route('/api/v1/movies', methods=['POST'])
    def movies():
        form = MovieForm()

        if form.validate_on_submit():
            # Get data
            title = form.title.data
            description = form.description.data
            poster = form.poster.data

            # Save file
            filename = secure_filename(poster.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            poster.save(upload_path)

            # Save to DB
            movie = Movie(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                "message": "Movie Successfully added",
                "title": title,
                "poster": filename,
                "description": description
            }), 201

        return jsonify(errors=form_errors(form)), 400
    
    @app.route('/api/v1/csrf-token', methods=['GET'])
    def get_csrf():
        return jsonify({'csrf_token': generate_csrf()})

# Keep your form_errors helper function
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)
    return error_messages

