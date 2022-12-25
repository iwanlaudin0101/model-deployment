import  re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class IdentifikasiValidate(FlaskForm):
    article = TextAreaField('Enter News Articles')
    submit = SubmitField('Predict')

    def validate_article(self, article):
        if article.data == '':
            raise ValidationError('Oopss! Field tidak boleh kosong.')

        inputs = re.sub(r'\W+', ' ', article.data).lower()
        inputs = inputs.split()
        
        if len(inputs) < 30:
            raise ValidationError('Oopss! Panjang minimal dokumen harus 30 karakter.') 

class IdentifikasiValidateTxt(FlaskForm):
    files = FileField('Enter News File', [DataRequired(), FileAllowed(['txt'], message='Oops! File yang anda masukan bukan txt')])
    submit = SubmitField('Predict')
