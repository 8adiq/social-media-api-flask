from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validates,ValidationError,validate,post_load
from models import User,Post,Like,Comment
from flask import jsonify
import re

# Schemas for each model
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    username = fields.String(required=True,validate=validate.Length(min=3,max=100))
    email = fields.Email(required=True)
    uid = fields.Integer(dump_only=True)
    password = fields.String(required=True,load_only=True,validate=validate.Length(min=6))

    # creating a model instance after loading from json
    @post_load
    def make_user(self,data,**kwargs):
        """"""
        return User(**data)

    # username and password validation here
    @validates('username')
    def validate_username(self,value):
        """"""
        if any(char in value for char in " !@#$%^&*()"):
            raise ValidationError('Username should not contain spaces or special characters')
        
    @validates('email')
    def validate_email(self,value):
        """"""
        existing_user = User.query.filter_by(email=value).first()
        if existing_user:
            raise ValidationError('Email already exists')
        
    @validates('password')
    def validate_password(self,value):
        """"""
        if len(value) <6: 
            raise ValidationError('Password must be at least 6 characters')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain an uppercase letter')
        if not re.search(r'[a-z]',value):
            raise ValidationError('Password must containt a lowercase letter')
        if not re.search(r'[!@#$%^&*()]',value):
            raise ValidationError('Password must contain a special character')

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    text = fields.String(required=False,validate=validate.Length(min=1,max=300))
    picture = fields.List(fields.Url(),required=False)
    video = fields.List(fields.Url(),required=False)
    created_at = fields.DateTime()
    uid = fields.Integer(dump_only=True)
    pid = fields.Integer(dump_only=True) 


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    cid = fields.Integer(dump_only=True)
    uid = fields.Integer(dum_only=True)
    pid = fields.Integer(required=True)

