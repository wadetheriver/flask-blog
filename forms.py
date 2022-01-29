from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField ,BooleanField, EmailField


class RegistrationForm(Form):
    first_name = StringField('First Name',
                             [validators.Length(min=1, max=50),
                              validators.Regexp("^[0-9a-zA-Z \-'_]+$",
                              message="First name must contain only letters, numbers and hyphens")
                              ])
    last_name = StringField('Last Name',
                            [validators.Length(min=1, max=50),
                             validators.Regexp("^[0-9a-zA-Z \-'_]+$",
                             message="Last name must contain only letters, numbers and hyphens")
                             ])
    username = StringField('Username',
                           [validators.Length(min=4, max=25),
                            validators.Regexp('^\w+$',
                                              message="Username must contain only letters numbers or underscore")
                            ])
    email = EmailField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match!")
    ])
    confirm = PasswordField('Confirm Password')
    # accept_rules = BooleanField('I promise to be nice.', [validators.InputRequired()])


# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    subtitle = StringField('Subtitle', [validators.Length(min=1, max=200)])
    excerpt = StringField('Excerpt', [validators.Length(min=1, max=400)])
    body = TextAreaField('Content', [validators.Length(min=1)])
