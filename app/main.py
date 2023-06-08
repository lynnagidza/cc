"""Main application routes and error handlers."""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Logic for the home page"""
    return render_template('home.html')

@main_bp.route('/about')
def about():
    """Logic for the about page"""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """Logic for the contact page"""
    return render_template('contact.html')

@main_bp.route('/cards')
def browse_cards():
    """Logic to fetch and display all available cards"""
    return render_template('cards.html')

@main_bp.route('/card/<int:card_id>')
def view_card(card_id):
    """Logic to fetch and display a specific card by its ID"""
    return render_template('card.html', card_id=card_id)

@main_bp.route('/cart')
def view_cart():
    """Logic to fetch and display the user's shopping cart"""
    return render_template('cart.html')

@main_bp.route('/checkout')
def checkout():
    """Logic for the checkout process and payment handling"""
    return render_template('checkout.html')

@main_bp.route('/order-confirmation')
def order_confirmation():
    """Logic to display the order confirmation page"""
    return render_template('order_confirmation.html')

# Add more routes as needed for additional functionality

# Error handlers
@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
