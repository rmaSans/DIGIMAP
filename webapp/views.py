from webapp import digiapp
from flask import render_template, request, redirect
import os

digiapp.config["IMAGE_UPLOADS"] = "F:\\Users\\Tongki\\Desktop\\Term 2\\DIGIMAP\\Project\\DIGIMAP\\webapp\\static\\img\\uploads"
@digiapp.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
      if request.files:
        image = request.files["image"]
        image.save(os.path.join(digiapp.config["IMAGE_UPLOADS"], image.filename))
        return redirect(request.url)
    return render_template('index.html')

@digiapp.route('/mechanisms')
def about():
    return render_template('mechanisms.html')

@digiapp.route('/team')
def team():
    return render_template('team.html')

#@digiapp.route('/upload-image', )
# def upload_image():
#     if request.method == "POST":
#         if request.files:
#           image = request.files["image"]
#           image.save(os.path.join(digiapp.config["IMAGE_UPLOADS"], image.filename))
#           return redirect(request.url)
    