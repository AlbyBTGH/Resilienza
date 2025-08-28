# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,TimeField, SelectField, DecimalField, SelectMultipleField, HiddenField, SubmitField, widgets, BooleanField, DateField, FileField, FormField, FieldList,PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length,  Email, EqualTo, NumberRange
from wtforms.validators import StopValidation
from datetime import datetime
from wtforms.validators import DataRequired, NumberRange, ValidationError


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)

class CustomSelectField(SelectField):
    def pre_validate(self, form):
        pass  # Bypassare la validazione delle scelte

class LogoutFormNoCSRF(FlaskForm):
    submit = SubmitField('Logout')

class LoginFormNoCSRF(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistratiForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        EqualTo('ripeti_password', message='Le password devono corrispondere')
    ])
    ripeti_password = PasswordField('Ripeti Password', validators=[DataRequired()])
    
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    
    conferma_invio_mail_pubblicitarie = BooleanField('conferma_invio_mail_pubblicitarie', validators=[Optional()])
    
    submit = SubmitField('submit')

class MagazziniForm(FlaskForm):
    DESCR = StringField('Descrizione', validators=[DataRequired()])
    NOTE = TextAreaField('Note', validators=[Optional()])

class LocazioneForm(FlaskForm):
    DESCR = StringField('Descrizione', validators=[DataRequired()])
    DT_FINE_VAL = DateField('Validità Fine', format='%Y-%m-%d', validators=[Optional()])
    NOTE = TextAreaField('Note', validators=[Optional()])
    ID_MAGAZZINO = SelectField('Magazzino', coerce=int, validators=[Optional()])
    # CAPIENZA_MAX = IntegerField('Capienza Massima', validators=[Optional()])  
    LOCAZIONE_FISSA = BooleanField ('Locazione fissa', validators=[Optional()])

class ContenitoreForm(FlaskForm):
    DESCR = StringField('Descrizione', validators=[DataRequired()])
    ID_MAGAZZINO = SelectField('Magazzino', coerce=int, validators=[Optional()])
    DT_FINE_VAL = DateField('Validità Fine', format='%Y-%m-%d', validators=[Optional()])
    NOTE = TextAreaField('Note', validators=[Optional()])

class CassoniForm:
    CODICE = StringField('Codice', validators=[DataRequired()])
    DESCRIZIONE = StringField('Descrizione', validators=[DataRequired()])
    
class MovimentiForm(FlaskForm):
    FL_IN_OUT = SelectField('Movimento', coerce=int, validators=[Optional()])
    TIPO_MOV_OUT = SelectField('Tipo movimento', coerce=int, validators=[Optional()])
    ID_MAGAZZINO = SelectField('Magazzino', coerce=int, validators=[Optional()])
    ID_LOCAZIONE = SelectField('Locazione', coerce=int, validators=[Optional()])
    ID_ARTICOLO = IntegerField('Codice Articolo', validators=[DataRequired()])
    DT_MOV = DateField('Data Movimento', format='%Y-%m-%d', validators=[DataRequired()])
    QTA = DecimalField('Quantità', places=2, validators=[DataRequired()])   
    ID_MAGAZZINO = SelectField('Magazzino', coerce=int, validators=[Optional()])
    ID_LOCAZIONE = SelectField('Locazione', coerce=int, validators=[Optional()])
    ID_CONTENITORE = IntegerField('ID Contenitore', coerce=int, validators=[Optional()])
    NOTE = TextAreaField('Note', validators=[Optional(), Length(max=500)])
    NUM_ANALISI = StringField('Numero Analisi', validators=[Optional(), Length(max=20)])
    SEND_MAIL = StringField('Send Mail', validators=[Optional(), Length(max=1)])

class CambioPasswordForm(FlaskForm):
    old_password = PasswordField('Vecchia Password', validators=[DataRequired()])
    new_password = PasswordField('Nuova Password', validators=[DataRequired(), Length(min=6)])
    conferma_new_password = PasswordField('Conferma Nuova Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Cambia Password')

class TipoUtenteForm(FlaskForm):
    DESCR = StringField('Ruolo', validators=[DataRequired()])  
    ORDINATORE = IntegerField ('Ordinatore', validators=[DataRequired()])
    VISUALIZZA_NOTIFICHE = BooleanField ('visualizza notifiche', validators=[Optional()])
    submit = SubmitField('Crea Tipo Utente')

# <--- AGGIUNTO QUI: ResetPasswordForm
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Richiedi Reset Password')

# <--- AGGIUNTO QUI: NuovaPasswordForm
class NuovaPasswordForm(FlaskForm):
    password = PasswordField('Nuova Password', validators=[DataRequired(), Length(min=6)])
    conferma_password = PasswordField('Conferma Nuova Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Imposta Nuova Password')
