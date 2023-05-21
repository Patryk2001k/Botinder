from app import app
from flask import render_template

@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def error_404(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(500)
def error_404(error):
    return render_template("errors/500.html"), 500
