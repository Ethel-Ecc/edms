from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


# add new dataset
class AddDatasetForm(FlaskForm):
    name_or_title = StringField('Name/Title', validators=[DataRequired(), Length(min=5)])
    distribution_license = SelectField('License',
                                       choices=[
                                            ('MIT License', 'MIT'),
                                            ('Apache License 2.0', 'Apache2.0'),
                                            ('BSD 3', 'BSD 3-Clause License (Revised)'),
                                            ('GPL v3', 'GNU General Public License v3'),
                                            ('LGPL v3', 'GNU Lesser General Public License v3 (LGPL-3.0)'),
                                                ],
                                       validators=[DataRequired()]
                                       )
    format = SelectField('Format',
                         choices=[
                             ('PDF', 'PDF'),
                             ('XML', 'XML'),
                             ('XLXS', 'XLXS'),
                             ('DOC', 'DOC'),
                             ('DOCX', 'DOCX'),
                             ('TEX', 'TEX'),
                         ],
                         validators=[DataRequired()])
    description = TextAreaField('Short Description', validators=[DataRequired(), Length(min=10)])
    download_url = StringField('Resource URL', validators=[DataRequired()])
    # download_url = FileField('Upload Resource', validators=[FileAllowed(['pdf', 'xlxs', 'doc', 'tex', 'docx', 'xml'])])
    submit = SubmitField('Save Dataset')
