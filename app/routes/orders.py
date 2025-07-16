from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user


orders_bp = Blueprint('orders', __name__)

