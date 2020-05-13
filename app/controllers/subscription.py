# app/controllers/subscription.py
# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.models.subscription import Subscription
from app.models.member import Member
import os
import datetime


@app.route("/subscription/edit/<int:member_id>")
@app.route("/subscription/edit/<int:member_id>/<int:subscription_id>", methods=['GET', 'POST'])
def edit_subscription(member_id, subscription_id=-1):
    member = Member.load(member_id)
    subscription = Subscription.load(subscription_id)
    return render_template("./member/edit_subscription.html", member=member, subscription=subscription, plan=member.plan)


@app.route("/subscription/save/<int:member_id>", methods=['GET', 'POST'])
@app.route("/subscription/save/<int:member_id>/<int:subscription_id>", methods=['GET', 'POST'])
def save_subscription(member_id, subscription_id=-1):
    if request.method == "POST":
        subscription = Subscription.load(subscription_id)
        subscription.member_id = member_id
        subscription.str_date = request.form.get("date")
        subscription.plan = request.form.get("plan")        
        subscription.save()
        return redirect(url_for("list_subscription", member_id=member_id))

    subscription = Subscription.load(subscription_id)
    return redirect(url_for("edit_subscription", member_id=member_id, 
                    subscription=subscription))


@app.route("/subscription/list")
@app.route('/subscription/list/<int:member_id>')
def list_subscription(member_id=-1):
    if member_id == -1:
        subscriptions = Subscription.load_all()
    else:
        subscriptions = Subscription.load_member(member_id)

    member = Member.load(member_id)
    return render_template("./member/list_member_subscription.html", subscriptions=subscriptions, member=member)


@app.route("/subscription/delete/<int:subscription_id>")
def delete_subscription(subscription_id):    
    Subscription.delete(subscription_id)
    return redirect(url_for('list_subscription'))
