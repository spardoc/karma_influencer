from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/comments.html')
def comments():
    return render_template('comments.html')

@main_bp.route('/analytics.html')
def analytics():
    return render_template('analytics.html')