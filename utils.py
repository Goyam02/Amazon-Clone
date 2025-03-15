from forms import SearchForm
from models import Category

def create_search_form():
    """Create and populate the search form with categories.
    
    Returns:
        SearchForm: An instance of the search form with category choices populated.
    """
    search_form = SearchForm()
    categories = Category.query.filter_by(parent_id=None).all()
    search_form.category.choices = [(0, 'All Categories')] + [(c.id, c.name) for c in categories]
    return search_form