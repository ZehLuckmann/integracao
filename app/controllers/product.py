# app/controllers/product.py
# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.models.product import Product
import os


@app.route("/product/edit")
@app.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
def edit_product(product_id=-1):
    product = Product.load(product_id)
    return render_template("./product/edit_product.html", product=product)


@app.route("/product/save", methods=['GET', 'POST'])
@app.route("/product/save/<int:product_id>", methods=['GET', 'POST'])
def save_product(product_id=-1):
    if request.method == "POST":
        product = Product.load(product_id)
        product.description = request.form.get("description")
        product.about = request.form.get("about")
        product.category = int(request.form.get("category", 99))
        product.str_price = request.form.get("price")
        product_photo = request.files.getlist("product_photo[]")
        product.save()

        dir_upload = "../static/resources/products/"
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
    return render_template("./product/list_product.html", products=products)


@app.route("/product/delete/<int:product_id>")
def delete_product(product_id):
    Product.delete(product_id)
    return redirect(url_for('list_product'))