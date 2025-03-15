import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import Product, Category, Review
from forms import ReviewForm, SearchForm, AddToCartForm
from extensions import db
from utils import create_search_form

product_bp = Blueprint('product', __name__)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    # Get the product
    product = Product.query.get_or_404(product_id)

    # Get reviews for this product
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()

    # Create review form if user is logged in
    review_form = None
    if current_user.is_authenticated:
        # Check if user already reviewed this product
        existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if not existing_review:
            review_form = ReviewForm()

    # Create add to cart form
    cart_form = AddToCartForm()
    cart_form.product_id.data = product_id

    # Create search form for header
    # search_form = SearchForm()
    # categories = Category.query.filter_by(parent_id=None).all()
    # search_form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    search_form = create_search_form()

    # Get related products (products in the same category)
    related_products = []
    if product.categories:
        category = product.categories[0]
        related_products = Product.query.join(Product.categories).filter(
            Category.id == category.id,
            Product.id != product_id
        ).limit(4).all()

    return render_template('product/detail.html',
                          product=product,
                          reviews=reviews,
                          review_form=review_form,
                          cart_form=cart_form,
                          search_form=search_form,
                          related_products=related_products)

@product_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)

    # Check if user already reviewed this product
    existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_review:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('product.product_detail', product_id=product_id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            product_id=product_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()

        flash('Your review has been submitted!', 'success')

    return redirect(url_for('product.product_detail', product_id=product_id))

@product_bp.route('/featured')
def featured():
    # Get featured products
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PRODUCTS_PER_PAGE', 20)

    products = Product.query.filter_by(is_featured=True).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Create search form for header
    # search_form = SearchForm()
    # categories = Category.query.filter_by(parent_id=None).all()
    # search_form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    search_form = create_search_form()

    return render_template('product/featured.html',
                          products=products,
                          search_form=search_form)
