from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, EqualTo, Length


def validate_email(form, field):
    if "@" not in str(field.data):
        raise ValidationError("Enter a valid email")

class RegisterationForm(FlaskForm):
    email = EmailField('', validators=[InputRequired(), validate_email], render_kw={"placeholder": "Email Id"})
    password = PasswordField('', validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('', validators=[InputRequired(), Length(min=8), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('', validators=[InputRequired(), Length(min=1)], render_kw={"placeholder": "Email Id"})
    password = PasswordField('', validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    remember = BooleanField()
    submit = SubmitField('Login')
