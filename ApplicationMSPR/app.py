# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from functions import *
import os
import random


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_name'  # Replace with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ammu@localhost:5432/postgres'
app.config['SECRET_KEY'] = os.urandom(24)  # Replace with a secret key
db = SQLAlchemy(app)


# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


# Define Review model
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id}>"


# Define Recommendation model
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Recommendation {self.id}>"


products = [
    # shoe1 shoes
    {'id': 'shoe1', 'name': 'nike 1.0', 'image': 's2.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 2.0', 'image': 's4.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 3.0', 'image': 's6.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 4.0', 'image': 's8.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 5.0', 'image': 's10.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 6.0', 'image': 's12.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 7.0', 'image': 's16.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 8.0', 'image': 's18.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 9.0', 'image': 's14.jpg', 'description': 'Shoe light weight and comfortable.'},
    {'id': 'shoe1', 'name': 'nike 10.0', 'image': 's20.jpg', 'description': 'Shoe light weight and comfortable.'},

    {'id': 'shoe2', 'name': 'Adidas 1.0', 'image': 's3.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 2.0', 'image': 's5.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 3.0', 'image': 's7.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 4.0', 'image': 's9.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 5.0', 'image': 's11.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 6.0', 'image': 's13.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 7.0', 'image': 's15.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 8.0', 'image': 's17.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 9.0', 'image': 's19.jpg', 'description': 'Stylish belt for any occasion.'},
    {'id': 'shoe2', 'name': 'Adidas 10.0', 'image': 's21.jpg', 'description': 'Stylish belt for any occasion.'},

    {'id': 'shoe3', 'name': 'Puma 1.0', 'image': 's22.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 2.0', 'image': 's23.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 3.0', 'image': 's24.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 4.0', 'image': 's25.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 5.0', 'image': 's26.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 6.0', 'image': 's27.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 7.0', 'image': 's28.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 8.0', 'image': 's29.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 9.0', 'image': 's30.jpg', 'description': 'Elegant and durable watch.'},
    {'id': 'shoe3', 'name': 'Puma 10.0', 'image': 's31.jpg', 'description': 'Elegant and durable watch.'},

    # sarees saree1
    {'id': 'saree1', 'name': 'Kanchi soft', 'image': 'saree1.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi hard', 'image': 'saree2.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi silk', 'image': 'saree3.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi smooth', 'image': 'saree4.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi ususal', 'image': 'saree5.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi rare cloth', 'image': 'saree6.jpg',
     'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi fabric', 'image': 'saree7.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi silk', 'image': 'saree8.jpg', 'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchi soft saree', 'image': 'saree9.jpg',
     'description': 'Beautiful like a wow sarees'},
    {'id': 'saree1', 'name': 'kanchipatu saree', 'image': 'saree10.jpg',
     'description': 'Beautiful like a wow sarees'},

    {'id': 'saree2', 'name': 'Gadwal Saree', 'image': 'saree11.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal silk', 'image': 'saree12.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal soft saree', 'image': 'saree13.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal silk saree', 'image': 'saree14.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal fabric', 'image': 'saree15.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal smooth', 'image': 'saree16.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal soft saree', 'image': 'saree17.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal Kancipattu', 'image': 'saree18.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal saree', 'image': 'saree19.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal colorful saree', 'image': 'saree20.jpg', 'description': 'good silk sarees'},
    {'id': 'saree2', 'name': 'Gadwal rare saree', 'image': 'saree21.jpg', 'description': 'good silk sarees'},

    {'id': 'saree3', 'name': 'Ikkat saree', 'image': 'saree22.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat fabric saree', 'image': 'saree23.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat smooth saree', 'image': 'saree24.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat soft saree', 'image': 'saree25.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat silk saree', 'image': 'saree26.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat saree', 'image': 'saree27.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat colorful saree', 'image': 'saree28.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat soft saree', 'image': 'saree29.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat rare saree', 'image': 'saree30.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat fabric saree', 'image': 'saree12.jpg', 'description': 'benaras pattu'},
    {'id': 'saree3', 'name': 'Ikkat soft saree', 'image': 'saree15.jpg', 'description': 'benaras pattu'},

    # watches
    {'id': 'watch1', 'name': 'Fastrack 1.0', 'image': 'Watches1.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 2.0', 'image': 'Watches2.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 3.0', 'image': 'Watches3.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 4.0', 'image': 'Watches4.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 5.0', 'image': 'Watches5.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 6.0', 'image': 'Watches6.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 7.0', 'image': 'Watches7.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 8.0', 'image': 'Watches8.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'Fastrack 9.0', 'image': 'Watches9.jpg', 'description': 'leather belt watches'},
    {'id': 'watch1', 'name': 'fastrack 10.0', 'image': 'Watches10.jpg', 'description': 'leather belt watches'},

    {'id': 'watch2', 'name': 'Fossil 1.0', 'image': 'Watches11.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 2.0', 'image': 'Watches12.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 3.0', 'image': 'Watches13.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 4.0', 'image': 'Watches14.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 5.0', 'image': 'Watches15.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 6.0', 'image': 'Watches16.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 7.0', 'image': 'Watches17.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 8.0', 'image': 'Watches18.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 9.0', 'image': 'Watches19.jpg', 'description': 'steel belt watches'},
    {'id': 'watch2', 'name': 'Fossil 10.0', 'image': 'Watches20.jpg', 'description': 'steel belt watches'},

    {'id': 'watch3', 'name': 'Titan 1.0', 'image': 'Watches21.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 2.0', 'image': 'Watches22.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 3.0', 'image': 'Watches23.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 4.0', 'image': 'Watches24.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 5.0', 'image': 'Watches25.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 6.0', 'image': 'Watches26.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 7.0', 'image': 'Watches27.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 8.0', 'image': 'Watches28.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 9.0', 'image': 'Watches29.jpg', 'description': 'smart watches'},
    {'id': 'watch3', 'name': 'Titan 10.0', 'image': 'Watches30.jpg', 'description': 'smart watches'},

    # tv
    {'id': 'TV1', 'name': 'Sony 36', 'image': 'Tv1.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 34', 'image': 'Tv2.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 38', 'image': 'Tv3.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 39', 'image': 'Tv4.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 36', 'image': 'Tv5.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 40', 'image': 'Tv6.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 38', 'image': 'Tv7.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 40', 'image': 'Tv8.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 40', 'image': 'Tv9.jpg', 'description': 'LED TV'},
    {'id': 'TV1', 'name': 'Sony 39', 'image': 'Tv10.jpg', 'description': 'LED TV'},

    {'id': 'TV2', 'name': 'LCD 36', 'image': 'Tv11.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 39', 'image': 'Tv12.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 38', 'image': 'Tv13.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 39', 'image': 'Tv14.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 40', 'image': 'Tv15.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 40', 'image': 'Tv16.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 40', 'image': 'Tv17.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 42', 'image': 'Tv18.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 40', 'image': 'Tv19.jpg', 'description': 'DOOM TV'},
    {'id': 'TV2', 'name': 'LCD 38', 'image': 'Tv20.jpg', 'description': 'DOOM TV'},

    {'id': 'TV3', 'name': 'LED 36', 'image': 'Tv21.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 40', 'image': 'Tv22.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 38', 'image': 'Tv23.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 39', 'image': 'Tv24.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 40', 'image': 'Tv25.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 42', 'image': 'Tv26.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 40', 'image': 'Tv27.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 38', 'image': 'Tv28.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 36', 'image': 'Tv29.jpg', 'description': 'SMART TV'},
    {'id': 'TV3', 'name': 'LED 38', 'image': 'Tv30.jpg', 'description': 'SMART TV'},

    # mencloth
    {'id': 'mencloth1', 'name': 'Trenz M', 'image': 'men1.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz S', 'image': 'men2.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XS', 'image': 'men13.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz L', 'image': 'men4.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XXS', 'image': 'men5.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz M', 'image': 'men6.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XL', 'image': 'men7.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XXl', 'image': 'men8.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XXXl', 'image': 'men9.jpg', 'description': 'torn cloth'},
    {'id': 'mencloth1', 'name': 'Trenz XL', 'image': 'men10.jpg', 'description': 'torn cloth'},

    {'id': 'mencloth2', 'name': 'Raymond S', 'image': 'men11.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond XS', 'image': 'men12.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond XXS', 'image': 'men13.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond M', 'image': 'men14.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond L', 'image': 'men15.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond XL', 'image': 'men16.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond XXL', 'image': 'men17.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond XXXl', 'image': 'men18.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond M', 'image': 'men19.jpg', 'description': 'bloody clothing pvt.ltd'},
    {'id': 'mencloth2', 'name': 'Raymond L', 'image': 'men20.jpg', 'description': 'bloody clothing pvt.ltd'},

    {'id': 'mencloth3', 'name': 'OTTO S', 'image': 'men21.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO M', 'image': 'men22.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO XS', 'image': 'men23.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO L', 'image': 'men24.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO M', 'image': 'men25.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO S', 'image': 'men26.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO XL', 'image': 'men27.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO XS', 'image': 'men28.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO XL', 'image': 'men29.jpg', 'description': 'once tried always used'},
    {'id': 'mencloth3', 'name': 'OTTO M', 'image': 'men30.jpg', 'description': 'once tried always used'},

    # Laptops
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop1.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop2.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop30.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop4.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop5.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop6.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop7.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop8.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop9.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop10.jpg', 'description': 'Idea pad'},
    {'id': 'lap1', 'name': 'lapt', 'image': 'Laptop11.jpg', 'description': 'Idea pad'},

    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop12.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop13.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop4.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop15.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop16.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop17.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop17.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop18.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop19.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop20.jpg', 'description': 'viva book'},
    {'id': 'lap2', 'name': 'lapt', 'image': 'Laptop21.jpg', 'description': 'viva book'},

    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop22.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop23.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop24.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop25.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop26.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop27.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop28.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop29.jpg', 'description': 'note book'},
    {'id': 'lap3', 'name': 'lapt', 'image': 'Laptop30.jpg', 'description': 'note book'},

    # dining
    {'id': 'din1', 'name': 'din', 'image': 'DT1.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT2.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT3.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT4.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT5.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT6.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT7.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT8.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT9.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT10.jpg', 'description': 'note book'},

    {'id': 'din2', 'name': 'dint', 'image': 'DT11.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT12.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT13.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT14.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT15.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT16.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT17.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT18.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT19.jpg', 'description': 'note book'},

    {'id': 'din3', 'name': 'dint', 'image': 'DT20.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT21.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT22.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT23.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT24.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT25.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT26.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT27.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT28.jpg', 'description': 'note book'},
    {'id': 'din1', 'name': 'din', 'image': 'DT29.jpg', 'description': 'note book'},
    {'id': 'din2', 'name': 'dint', 'image': 'DT30.jpg', 'description': 'note book'},
    {'id': 'din3', 'name': 'dint', 'image': 'DT1.jpg', 'description': 'note book'},

    {'id': 'VAS1', 'name': 'din', 'image': 'v1.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v11.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v12.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v13.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v14.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v15.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v16.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v17.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v18.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v19.jpg', 'description': 'note book'},
    {'id': 'VAS1', 'name': 'din', 'image': 'v2.jpg', 'description': 'note book'},

    {'id': 'VAS2', 'name': 'dint', 'image': 'v2.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v3.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v4.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v5.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v6.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v7.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v8.jpeg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v9.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v10.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v13.jpg', 'description': 'note book'},
    {'id': 'VAS2', 'name': 'dint', 'image': 'v20.jpg', 'description': 'note book'},

    {'id': 'VAS3', 'name': 'dint', 'image': 'v21.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v22.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v23.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v24.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v25.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v26.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v27.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v28.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v29.jpg', 'description': 'note book'},
    {'id': 'VAS3', 'name': 'dint', 'image': 'v30.jpg', 'description': 'note book'},

    # washes
    {'id': 'WAS1', 'name': 'din', 'image': 'wm1.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm10.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm11.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm12.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm13.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm14.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm15.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm16.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm17.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm18.jpg', 'description': '10kg'},
    {'id': 'WAS1', 'name': 'din', 'image': 'wm19.jpg', 'description': '10kg'},

    {'id': 'WAS2', 'name': 'dint', 'image': 'wm20.jpg', 'description': '20kg'},

    {'id': 'WAS2', 'name': 'dint', 'image': 'wm21.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm22.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm23.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm24.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm25.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm26.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm27.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm28.jpg', 'description': '20kg'},
    {'id': 'WAS2', 'name': 'dint', 'image': 'wm29.jpg', 'description': '20kg'},

    {'id': 'WAS3', 'name': 'dint', 'image': 'wm30.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm2.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm3.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm4.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm5.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm6.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm7.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm8.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm9.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm10.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm17.jpg', 'description': '30kg'},
    {'id': 'WAS3', 'name': 'dint', 'image': 'wm19.jpg', 'description': '30kg'}

    # Add more products as needed
]


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Routes
@app.route('/')
def home():
    # Show products
    # products = [...]  # Define your products here

    return render_template('home.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error='Email already exists')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/write_review', methods=['GET', 'POST'])
@login_required
def write_review():
    pd = [
        {'id': 'shoe1', 'name': 'Product A', 'image': 's2.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe2', 'name': 'Product b', 'image': 's3.jpg', 'description': 'Shoe light weight and comfortable.'},
        {'id': 'shoe3', 'name': 'Product c', 'image': 's24.jpg', 'description': 'Shoe light weight and comfortable.'},

        {'id': 'saree1', 'name': 'saree', 'image': 's31.jpg', 'description': 'Beautiful like a wow sarees'},
        {'id': 'saree2', 'name': 'saree', 'image': 's31.jpg', 'description': 'good silk sarees'},
        {'id': 'saree3', 'name': 'saree', 'image': 's31.jpg', 'description': 'benaras pattu'},

        {'id': 'watch1', 'name': 'saree', 'image': 's31.jpg', 'description': 'leather belt watches'},
        {'id': 'watch2', 'name': 'saree', 'image': 's31.jpg', 'description': 'steel belt watches'},
        {'id': 'watch3', 'name': 'saree', 'image': 's31.jpg', 'description': 'smart watches'},

        {'id': 'TV1', 'name': 'saree', 'image': 's31.jpg', 'description': 'LED TV'},
        {'id': 'TV2', 'name': 'saree', 'image': 's31.jpg', 'description': 'DOOM TV'},
        {'id': 'TV3', 'name': 'saree', 'image': 's31.jpg', 'description': 'SMART TV'},

        {'id': 'mencloth1', 'name': 'saree', 'image': 'men1.jpg', 'description': 'torn cloth'},
        {'id': 'mencloth2', 'name': 'saree', 'image': 'men2.jpg', 'description': 'torn cloth'},
        {'id': 'mencloth3', 'name': 'saree', 'image': 'men13.jpg', 'description': 'torn cloth'},

        {'id': 'lap1', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'Idea pad'},
        {'id': 'lap2', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'viva book'},
        {'id': 'lap3', 'name': 'lapt', 'image': 'lap.jpg', 'description': 'note book'},

        {'id': 'din1', 'name': 'din', 'image': 'DT.jpg', 'description': 'note book'},
        {'id': 'din2', 'name': 'dint', 'image': 'DT.jpg', 'description': 'note book'},
        {'id': 'din3', 'name': 'dint', 'image': 'DT.jpg', 'description': 'note book'},

        {'id': 'VAS1', 'name': 'din', 'image': 'v1.jpg', 'description': 'note book'},
        {'id': 'VAS2', 'name': 'dint', 'image': 'v.jpg', 'description': 'note book'},
        {'id': 'VAS3', 'name': 'dint', 'image': 'v.jpg', 'description': 'note book'},

        {'id': 'WAS1', 'name': 'din', 'image': 'wm1.jpg', 'description': 'note book'},
        {'id': 'WAS2', 'name': 'dint', 'image': 'wm.jpg', 'description': 'note book'},
        {'id': 'WAS3', 'name': 'dint', 'image': 'wm.jpg', 'description': 'note book'}

    ]
    random.shuffle(products)
    random.shuffle(pd)

    return render_template('write_review.html', pd=pd, products=products)


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        product_id = request.form['id']
        text = request.form['review']
        user_id = session['user_id']
        new_review = Review(product_id=product_id, text=text, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()

        # Perform sentiment analysis and get recommendations
        sentiment = perform_sentiment_analysis(text)
        recommendations = get_recommendations(sentiment, product_id)

        # Save recommendations
        for recommendation in recommendations:
            new_recommendation = Recommendation(description=recommendation['description'],
                                                product_id=recommendation['id'], user_id=user_id,
                                                image=recommendation['image'])
            db.session.add(new_recommendation)
        db.session.commit()
        random.shuffle(recommendations)

        return render_template('review_result.html', sentiment=sentiment, recommendations=recommendations)
    return render_template('write_review.html')


@app.route('/my_reviews')
@login_required
def my_reviews():
    user_id = session['user_id']
    reviews = Review.query.filter_by(user_id=user_id).all()
    return render_template('my_reviews.html', reviews=reviews)


@app.route('/my_recommendations')
@login_required
def my_recommendations():
    user_id = session['user_id']
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()
    random.shuffle(recommendations)

    return render_template('my_recommendations.html', recommendations=recommendations)


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
