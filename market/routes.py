from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user,logout_user, login_required, current_user

@app.route('/') #one step before func, root url of website
#@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required 
def market_page():
    # items=[
    #     {'id':1, 'name':'Phone', 'barcode':'893212299897', 'price':500},
    #     {'id':2, 'name':'Laptop', 'barcode':'123985473165', 'price':900},
    #     {'id':3, 'name':'Keyboard', 'barcode':'231985128446', 'price':150}    
    # ]
    purchase_form= PurchaseItemForm()
    selling_form= SellItemForm()
    #if purchase_form.validate_on_submit():
        #print(purchase_form.__dict__)
        #print(purchase_form['submit'])
        #print(purchase_form['purchased_item'])
        #print(request.form.get('purchased_item'))
    if request.method=="POST":
        #purchase item logic
        purchased_item= request.form.get('purchased_item')
        p_item_object= Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
                if current_user.can_purchase(p_item_object):
                    # p_item_object.owner=current_user.id
                    # current_user.budget-=p_item_object.price
                    # db.session.commit()
                    p_item_object.buy(current_user)
                    flash(f"Congratulations! You've purchased {p_item_object.name} for Rs.{p_item_object.price}.", category='success')
                else:
                    flash(f"Unfortunately, you don't have enough budget to purchase {p_item_object.name}.", category='danger')
        
        #sell item logic
        sold_item= request.form.get('sold_item')
        s_item_object= Item.query.filter_by(name=sold_item).first()
        if s_item_object:
                if current_user.can_sell(s_item_object):
                    s_item_object.sell(current_user)
                    flash(f"Congratulations! You've sold {s_item_object.name} for Rs.{s_item_object.price}.", category='success')
                else:
                    flash(f"Something went wrong while trying to sell {s_item_object.name}.", category='danger')
        return redirect(url_for('market_page'))
    
    if request.method=="GET":
        items= Item.query.filter_by(owner=None)
        owned_items= Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)
# @app.route('/about/<username>')
# def about_page(username):
#     return f'<h1>Hello {username}</h1>'

@app.route('/register', methods=['GET','POST'])
def register_page():
    form= RegisterForm()
    if form.validate_on_submit():
        user_to_create= User(username=form.username.data, 
                            email_address= form.email_address.data,
                            password= form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'You have successfully registered and are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors!={}: #if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error creating the account: {err_msg}', category='danger')
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'You have successfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Either username or password is incorrect. Please try again.', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have logged out.", category='info')
    return redirect(url_for('home_page'))

#decorators are fns that execute before the actual fn
