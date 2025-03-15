from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import current_user, login_required
from models import Product, Category, CartItem, Order, OrderItem, User
from forms import AddToCartForm, CheckoutForm, SearchForm
from extensions import db
from datetime import datetime
from utils import create_search_form

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    form = AddToCartForm()

    if form.validate_on_submit():
        product_id = form.product_id.data
        quantity = form.quantity.data

        # Validate product exists
        product = Product.query.get_or_404(product_id)

        # Check stock availability
        if quantity > product.stock:
            flash(f'Sorry, only {product.stock} items are available.', 'warning')
            return redirect(url_for('product.product_detail', product_id=product_id))

        # If user is logged in, save to DB
        if current_user.is_authenticated:
            # Check if item already in cart
            cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

            if cart_item:
                # Update quantity
                cart_item.quantity += quantity
            else:
                # Add new item
                cart_item = CartItem(
                    user_id=current_user.id,
                    product_id=product_id,
                    quantity=quantity
                )
                db.session.add(cart_item)

            db.session.commit()

        # For non-logged in users, use session
        else:
            # Initialize cart if not exists
            if 'cart' not in session:
                session['cart'] = {}

            # Update cart
            cart = session['cart']
            product_id_str = str(product_id)

            if product_id_str in cart:
                cart[product_id_str] += quantity
            else:
                cart[product_id_str] = quantity

            session['cart'] = cart

        flash(f'{product.name} added to your cart!', 'success')
        return redirect(url_for('product.product_detail', product_id=product_id))

    # If form validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}", 'danger')

    return redirect(url_for('main.index'))

@cart_bp.route('/')
def view_cart():
    cart_items = []
    total = 0

    # Get cart items from database if user is logged in
    if current_user.is_authenticated:
        db_cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

        for item in db_cart_items:
            product = item.product
            subtotal = product.price * item.quantity
            cart_items.append({
                'id': item.id,
                'product': product,
                'quantity': item.quantity,
                'subtotal': subtotal
            })
            total += subtotal

    # Otherwise get from session
    else:
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                if product:
                    subtotal = product.price * quantity
                    cart_items.append({
                        'id': product_id,
                        'product': product,
                        'quantity': quantity,
                        'subtotal': subtotal
                    })
                    total += subtotal

    # Create search form for header
    # search_form = SearchForm()
    # categories = Category.query.filter_by(parent_id=None).all()
    # search_form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    search_form = create_search_form()

    return render_template('cart/cart.html',
                          cart_items=cart_items,
                          total=total,
                          search_form=search_form)

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    quantity = request.form.get('quantity', type=int)

    if not quantity or quantity < 1:
        flash('Invalid quantity', 'danger')
        return redirect(url_for('cart.view_cart'))

    # Update for logged in users
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
        product = cart_item.product

        # Check stock
        if quantity > product.stock:
            flash(f'Only {product.stock} items available', 'warning')
            return redirect(url_for('cart.view_cart'))

        cart_item.quantity = quantity
        db.session.commit()

    # Update for non-logged in users
    else:
        if 'cart' in session:
            cart = session['cart']
            product_id = str(item_id)

            if product_id in cart:
                # Check stock
                product = Product.query.get(int(product_id))
                if quantity > product.stock:
                    flash(f'Only {product.stock} items available', 'warning')
                    return redirect(url_for('cart.view_cart'))

                cart[product_id] = quantity
                session['cart'] = cart

    flash('Cart updated', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>')
def remove_from_cart(item_id):
    # Remove for logged in users
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
        db.session.delete(cart_item)
        db.session.commit()

    # Remove for non-logged in users
    else:
        if 'cart' in session:
            cart = session['cart']
            product_id = str(item_id)

            if product_id in cart:
                del cart[product_id]
                session['cart'] = cart

    flash('Item removed from cart', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Get cart items
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    # Redirect if cart is empty
    if not cart_items:
        flash('Your cart is empty', 'info')
        return redirect(url_for('cart.view_cart'))

    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create checkout form
    form = CheckoutForm()

    # Process form submission
    if form.validate_on_submit():
        # Create order
        order = Order(
            user_id=current_user.id,
            order_date=datetime.utcnow(),
            status='pending',
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_state=form.shipping_state.data,
            shipping_postal_code=form.shipping_postal_code.data,
            shipping_country=form.shipping_country.data,
            payment_method=form.payment_method.data,
            total_amount=total
        )

        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items from cart items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)

            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity

            # Delete cart item
            db.session.delete(cart_item)

        db.session.commit()

        flash('Your order has been placed!', 'success')
        return redirect(url_for('main.index'))

    # Pre-populate form with user profile data
    if request.method == 'GET':
        form.shipping_address.data = current_user.address
        form.shipping_city.data = current_user.city
        form.shipping_state.data = current_user.state
        form.shipping_postal_code.data = current_user.postal_code
        form.shipping_country.data = current_user.country

    # Create search form for header
    # search_form = SearchForm()
    # categories = Category.query.filter_by(parent_id=None).all()
    # search_form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    search_form = create_search_form()
    return render_template('cart/checkout.html',
                          form=form,
                          cart_items=cart_items,
                          total=total,
                          search_form=search_form)
