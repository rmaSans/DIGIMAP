# from webapp import digiapp
# from flask import render_template, request, redirect
# from pathlib import Path
# import os

# script_dir = Path(__file__).parent
# images_dir = script_dir.parent /"webapp"/ "static" / "img" / "uploads"
# @digiapp.route('/', methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#       if request.files:
#         image = request.files["image"]
#         image.save(os.path.join(images_dir, "gs_image.jpg"))
#         return redirect(request.url)
#     return render_template('index.html')

# @digiapp.route('/mechanisms')
# def about():
#     return render_template('mechanisms.html')

# @digiapp.route('/team')
# def team():
#     return render_template('team.html')

    