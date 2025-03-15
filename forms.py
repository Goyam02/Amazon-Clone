from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, TextAreaField,
    SelectField, FloatField, IntegerField, SubmitField,
    HiddenField, DecimalField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, NumberRange,
    Optional, ValidationError, Regexp
)
from models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    address = StringField('Address', validators=[Length(max=256)])
    city = StringField('City', validators=[Length(max=64)])
    state = StringField('State/Province', validators=[Length(max=64)])
    postal_code = StringField('Postal Code', validators=[Length(max=20)])
    country = StringField('Country', validators=[Length(max=64)])
    phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Update Profile')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount_price = FloatField('Discount Price', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[NumberRange(min=0)], default=0)
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    brand = StringField('Brand', validators=[Length(max=100)])
    categories = SelectField('Category', coerce=int)
    is_featured = BooleanField('Featured Product')
    submit = SubmitField('Save Product')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Search')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Length(max=256)])
    image = FileField('Category Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    parent_category = SelectField('Parent Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Category')


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'),
                                           (4, '4 - Very Good'), (5, '5 - Excellent')],
                        coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Length(max=500)])
    submit = SubmitField('Submit Review')


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    product_id = HiddenField()
    submit = SubmitField('Add to Cart')


class CheckoutForm(FlaskForm):
    shipping_address = StringField('Address', validators=[DataRequired(), Length(max=256)])
    shipping_city = StringField('City', validators=[DataRequired(), Length(max=64)])
    shipping_state = StringField('State/Province', validators=[DataRequired(), Length(max=64)])
    shipping_postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    shipping_country = StringField('Country', validators=[DataRequired(), Length(max=64)])
    payment_method = SelectField('Payment Method',
                                choices=[('cod', 'Cash on Delivery'),
                                        ('card', 'Credit/Debit Card')],
                                validators=[DataRequired()])
    # Credit card fields (shown only if payment method is card)
    card_number = StringField('Card Number', validators=[
        Regexp(r'^\d{16}$', message='Card number must be 16 digits')])
    card_expiry = StringField('Expiry (MM/YY)', validators=[
        Regexp(r'^\d{2}/\d{2}$', message='Expiry date must be in MM/YY format')])
    card_cvv = StringField('CVV', validators=[
        Regexp(r'^\d{3}$', message='CVV must be 3 digits')])
    submit = SubmitField('Place Order')


class BannerForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=100)])
    description = StringField('Description', validators=[Length(max=250)])
    image = FileField('Banner Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    link_url = StringField('Link URL', validators=[Length(max=256)])
    position = IntegerField('Position', default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Banner')
