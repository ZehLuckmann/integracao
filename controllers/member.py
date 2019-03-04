#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
from application import app
from models.member import Member
from models.event import Event
from models.financial import Financial
from models.product import Product
from models.team import Team
from models.training import Training
import os
import datetime


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
