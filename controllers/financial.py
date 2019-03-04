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