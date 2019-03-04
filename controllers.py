#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
from application import app
from models import *
import os
import datetime

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/calendar")
def calendar():
    events = Event.load_all()
    return render_template("calendar.html", events=events)

@app.route("/member/edit")
@app.route("/member/edit/<int:member_id>", methods=['GET', 'POST'])
def edit_member(member_id=-1):
    member = Member.load(member_id)
    return render_template("edit_member.html", member=member)

@app.route("/member/save", methods=['GET', 'POST'])
@app.route("/member/save/<int:member_id>", methods=['GET', 'POST'])
def save_member(member_id=-1):
    if request.method == "POST":
        member = Member.load(member_id)
        member.username = request.form.get("username")
        member.name = request.form.get("name")
        member.nickname = request.form.get("nickname")
        member.password = request.form.get("password")
        member.email = request.form.get("email")
        member.adress = request.form.get("adress")
        member.city = request.form.get("city")
        member.state = request.form.get("state")
        member.telephone = request.form.get("telephone")
        member.about = request.form.get("about")
        profile_photo = request.files.getlist("profile_photo[]")
        member.save()

        dir_upload = "./static/resources/profiles/"
        if not os.path.exists(dir_upload):
            os.makedirs(dir_upload)
        member_id = member.id
        for img in profile_photo:
            img.save(os.path.join(dir_upload, str(member_id) + ".png"))

        return redirect(url_for("list_member"))

@app.route("/member/")
@app.route('/member/list')
def list_member():
    members = Member.load_all()
    return render_template("list_member.html", members=members)

@app.route("/member/delete/<int:member_id>")
def delete_member(member_id):
    Member.delete(member_id)
    return redirect(url_for('list_member'))

@app.route("/member/card/<int:member_id>")
def card_member(member_id):
    member = Member.load(member_id)
    return render_template("card_member.html", member=member)


#FINANCIAL
@app.route("/financial/edit")
@app.route("/financial/edit/<int:financial_id>", methods=['GET', 'POST'])
def edit_financial(financial_id=-1):
    financial = Financial.load(financial_id)
    return render_template("edit_financial.html", financial=financial)

@app.route("/financial/save", methods=['GET', 'POST'])
@app.route("/financial/save/<int:financial_id>", methods=['GET', 'POST'])
def save_financial(financial_id=-1):
    if request.method == "POST":
        financial = Financial.load(financial_id)
        financial.str_date = request.form.get("date")
        financial.str_value = request.form.get("value")
        financial.description = request.form.get("description")
        financial.type = int(request.form.get("type"))
        financial.category = int(request.form.get("category"))
        financial.save()

        return redirect(url_for("list_financial"))

    return redirect(url_for("edit_financial", financial_id=financial_id))

@app.route("/financial/")
@app.route('/financial/list')
def list_financial():
    financials = Financial.load_all()
    return render_template("list_financial.html", financials=financials)

@app.route("/financial/delete/<int:financial_id>")
def delete_financial(financial_id):
    Financial.delete(financial_id)
    return redirect(url_for('list_financial'))

#TEAM
@app.route("/team/edit")
@app.route("/team/edit/<int:team_id>", methods=['GET', 'POST'])
def edit_team(team_id=-1):
    team = Team.load(team_id)
    return render_template("edit_team.html", team=team)

@app.route("/team/save", methods=['GET', 'POST'])
@app.route("/team/save/<int:team_id>", methods=['GET', 'POST'])
def save_team(team_id=-1):
    if request.method == "POST":
        team = Team.load(team_id)
        team.description = request.form.get("description")
        team.save()

        return redirect(url_for("list_team"))

    return redirect(url_for("edit_team", team_id=team_id))

@app.route("/team/")
@app.route('/team/list')
def list_team():
    teams = Team.load_all()
    return render_template("list_team.html", teams=teams)


@app.route("/team/delete/<int:team_id>")
def delete_team(team_id):
    Team.delete(team_id)
    return redirect(url_for('list_team'))

@app.route("/team/member/edit")
@app.route("/team/member/edit/<int:team_id>", methods=['GET', 'POST'])
def edit_team_member(team_id=-1):
    team = Team.load(team_id)
    members = Member.load_all()
    return render_template("edit_team_member.html", team=team, members=members)

@app.route("/team/member/save/<int:team_id>", methods=['GET', 'POST'])
def save_team_member(team_id):
    if request.method == "POST":
        team = Team.load(team_id)
        team.add_member(int(request.form.get("team_member")))
        team.save()

        return redirect(url_for("edit_team_member", team_id=team_id))

    return redirect(url_for("edit_team_member", team_id=team_id))

@app.route("/training/edit/<int:team_id>")
@app.route("/training/edit/<int:team_id>/<int:training_id>", methods=['GET', 'POST'])
def edit_training(team_id, training_id=-1):
    team = Team.load(team_id)
    training = Training.load(training_id)
    return render_template("edit_training.html", team=team, training=training )

@app.route("/team/delete/<int:team_id>/<int:member_id>")
def delete_team_member(team_id, member_id):
    team = Team.load(team_id)
    team.delete_member(member_id)
    return redirect(url_for('edit_team_member', team_id=team_id))

@app.route("/training/save/<int:team_id>", methods=['GET', 'POST'])
@app.route("/training/save/<int:team_id>/<int:training_id>", methods=['GET', 'POST'])
def save_training(team_id, training_id=-1):
    if request.method == "POST":
        training = Training.load(training_id)
        training.team_id = team_id
        training.str_date = request.form.get("date")
        training.save()

        return redirect(url_for("list_team"))

    training = Training.load(training_id)
    return redirect(url_for("edit_training", team_id=team_id, training=training))


@app.route("/training/list")
@app.route('/training/list/<int:team_id>')
def list_training(team_id=-1):
    if team_id == -1:
        trainings = Training.load_all()
    else:
        trainings = Training.load_team(team_id)

    team = Team.load(team_id)
    return render_template("list_training.html", trainings=trainings, team=team)

@app.route("/training/delete/<int:training_id>")
def delete_training(training_id):
    Training.delete(training_id)
    return redirect(url_for('list_training'))

#EVENT
@app.route("/event/edit")
@app.route("/event/edit/<int:event_id>", methods=['GET', 'POST'])
def edit_event(event_id=-1):
    event = Event.load(event_id)
    return render_template("edit_event.html", event=event)

@app.route("/event/save", methods=['GET', 'POST'])
@app.route("/event/save/<int:event_id>", methods=['GET', 'POST'])
def save_event(event_id=-1):
    if request.method == "POST":
        event = Event.load(event_id)
        event.description = request.form.get("description")
        event.str_date = request.form.get("date")
        event.save()

        return redirect(url_for("list_event"))

@app.route("/event/")
@app.route('/event/list')
def list_event():
    events = Event.load_all()
    return render_template("list_event.html", events=events)

@app.route("/event/delete/<int:event_id>")
def delete_event(event_id):
    Event.delete(event_id)
    return redirect(url_for('list_event'))

#PRODUCT
@app.route("/product/edit")
@app.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
def edit_product(product_id=-1):
    product = Product.load(product_id)
    return render_template("edit_product.html", product=product)

@app.route("/product/save", methods=['GET', 'POST'])
@app.route("/product/save/<int:product_id>", methods=['GET', 'POST'])
def save_product(product_id=-1):
    if request.method == "POST":
        product = Product.load(product_id)
        product.description = request.form.get("description")
        product.about = request.form.get("about")
        product.str_price = request.form.get("price")
        product_photo = request.files.getlist("product_photo[]")
        product.save()

        dir_upload = "./static/resources/products/"
        if not os.path.exists(dir_upload):
            os.makedirs(dir_upload)
        product_id = product.id
        for img in product_photo:
            img.save(os.path.join(dir_upload, str(product_id) + ".png"))

        return redirect(url_for("list_product"))

@app.route("/product/")
@app.route('/product/list')
def list_product():
    products = Product.load_all()
    return render_template("list_product.html", products=products)

@app.route("/product/delete/<int:product_id>")
def delete_product(product_id):
    Product.delete(product_id)
    return redirect(url_for('list_product'))