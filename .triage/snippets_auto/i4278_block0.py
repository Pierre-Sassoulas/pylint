from flask_wtf import FlaskForm


class TestForm(FlaskForm):
    pass


form = TestForm()
print(form.errors)

