from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from models import Product, Category, Banner
from forms import SearchForm
from extensions import db
from utils import create_search_form

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    # Get featured products
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    
    # Get categories for navigation
    categories = Category.query.filter_by(parent_id=None).all()
    
    # Get active banners for carousel
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.position).all()
    
    # Get products by category for homepage sections
    category_sections = []
    main_categories = Category.query.filter_by(parent_id=None).limit(5).all()
    
    for category in main_categories:
        products = Product.query.join(Product.categories).filter(Category.id == category.id).limit(4).all()
        if products:
            category_sections.append({
                'category': category,
                'products': products
            })
    
    # Create search form
    search_form = create_search_form()
    
    return render_template('index.html', 
                          featured_products=featured_products,
                          categories=categories,
                          banners=banners,
                          category_sections=category_sections,
                          search_form=search_form)

@main_bp.route('/search')
def search():
    # Get query parameters
    query = request.args.get('query', '')
    category_id = request.args.get('category', 0, type=int)
    
    # Create search form and populate with request data
    search_form = create_search_form()
    search_form.query.data = query
    search_form.category.data = category_id
    
    # Perform search query
    products_query = Product.query
    
    if query:
        products_query = products_query.filter(
            Product.name.ilike(f'%{query}%') | 
            Product.description.ilike(f'%{query}%') |
            Product.brand.ilike(f'%{query}%')
        )
    
    if category_id > 0:
        products_query = products_query.join(Product.categories).filter(Category.id == category_id)
    
    # Paginate results
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PRODUCTS_PER_PAGE', 20)
    products = products_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('search_results.html', 
                          query=query,
                          selected_category=category_id,
                          products=products,
                          search_form=search_form)

@main_bp.route('/category/<int:category_id>')
def category(category_id):
    # Get the category
    category = Category.query.get_or_404(category_id)
    
    # Get all subcategories
    subcategories = Category.query.filter_by(parent_id=category_id).all()
    
    # Get products in this category (and subcategories)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PRODUCTS_PER_PAGE', 20)
    
    # Base query - products directly in this category
    products_query = Product.query.join(Product.categories).filter(Category.id == category_id)
    
    # Add subcategory products
    if subcategories:
        subcategory_ids = [subcat.id for subcat in subcategories]
        products_query = products_query.union(
            Product.query.join(Product.categories).filter(Category.id.in_(subcategory_ids))
        )
    
    # Paginate
    products = products_query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Create search form
    search_form = create_search_form()
    
    # Featured products for specialized templates
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    
    # Best sellers for specialized templates
    best_sellers = Product.query.join(Product.categories).filter(
        Category.id == category_id
    ).order_by(Product.price.desc()).limit(4).all()
    
    # Check if we should use a specialized template
    template = 'category.html'
    
    # Use specialized template for Electronics category
    if category.name == "Electronics":
        template = 'category_electronics.html'
    
    # Use specialized template for Clothing category
    elif category.name == "Clothing":
        template = 'category_clothing.html'
    
    return render_template(template, 
                          category=category,
                          subcategories=subcategories,
                          products=products,
                          search_form=search_form,
                          featured_products=featured_products,
                          best_sellers=best_sellers)

@main_bp.route('/about')
def about():
    search_form = create_search_form()
    return render_template('about.html', search_form=search_form)

@main_bp.route('/contact')
def contact():
    search_form = create_search_form()
    return render_template('contact.html', search_form=search_form)