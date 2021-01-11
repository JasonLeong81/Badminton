from flask import Blueprint, render_template

errors = Blueprint('errors',__name__)



@errors.app_errorhandler(404) # use app_errorhandler so that this error would work in our entire app rather than just in this blueprint
def error_404(error):
    return render_template('errors/404.html'), 404 # 404 is the status code, in render_template the second parameter is always the status code and it is default to 200 so that thats why
    # we didnt specify it previously

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500