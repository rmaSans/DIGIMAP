from flask import Flask,render_template, request, redirect
from pathlib import Path
import os
from colorizers import *
import argparse
import matplotlib.pyplot as plt
from PIL import Image

app = Flask(__name__)

script_dir = Path(__file__).parent
images_dir = script_dir/ "static" / "img" / "uploads"
gs_dir = images_dir / "gs_image.jpg"
colorized_dir = script_dir / "static" / "img" / "colorized"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
      if request.files:
        image = request.files["image"]
        image.save(os.path.join(images_dir, "gs_image.jpg"))
        return redirect(request.url)
    return render_template('index.html')

@app.route('/mechanisms')
def about():
    return render_template('mechanisms.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/colorize')
def colorize():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--img_path', type=str, default='imgs/ansel_adams3.jpg')
    parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
    parser.add_argument('-o','--save_prefix', type=str, default='saved', help='will save into this file with {eccv16.png, siggraph17.png} suffixes')
    opt = parser.parse_args()

    # load colorizers
    colorizer_eccv16 = eccv16(pretrained=True).eval()
    colorizer_siggraph17 = siggraph17(pretrained=True).eval()
    if(opt.use_gpu):
        colorizer_eccv16.cuda()
        colorizer_siggraph17.cuda()

    # default size to process images is 256x256
    # grab L channel in both original ("orig") and resized ("rs") resolutions
    img = load_img(opt.img_path)
    (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
    if(opt.use_gpu):
        tens_l_rs = tens_l_rs.cuda()

    # colorizer outputs 256x256 ab map
    # resize and concatenate to original L channel
    img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
    out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

    plt.imsave('%s_eccv16.png'%opt.save_prefix, out_img_eccv16)
    plt.imsave('%s_siggraph17.png'%opt.save_prefix, out_img_siggraph17)    
    
