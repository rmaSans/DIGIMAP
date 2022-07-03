import os
import matplotlib.pyplot as plt
from flask import Flask, flash, render_template, request, redirect, send_file
from zipfile import ZipFile
from pathlib import Path
from colorizers import *
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'Some Random Bytes'
script_dir = Path(__file__).parent
uploads_dir = script_dir/ "static" / "img" / "uploads"
colorized_dir = script_dir /"static" / "img" / "colorized"
gs_dir = uploads_dir / "gs_image.jpg"
eccv_dir = script_dir / "static" / "img" / "colorized" / "eccv.png"
siggraph_dir = script_dir / "static" / "img" / "colorized" / "siggraph.png"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=["GET", "POST"])
def uploading():
    if request.files:
        image = request.files["image"]
        if image.filename == '':
            flash('Choose an image')
            return render_template('index.html')
        else:
            image.save(os.path.join(uploads_dir, "gs_image.jpg"))
            return redirect(request.url)

@app.route('/mechanisms')
def about():
    return render_template('mechanisms.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/colorize')
def colorize():

    if len(os.listdir(uploads_dir)) > 1:
        colorizer_eccv16 = eccv16(pretrained=True).eval()
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()

        # default size to process images is 256x256
        # grab L channel in both original ("orig") and resized ("rs") resolutions
        img = load_img(gs_dir)
        (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))

        img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        plt.imsave(eccv_dir,out_img_eccv16)
        plt.imsave(siggraph_dir ,out_img_siggraph17)
    else:
        flash("No files to colorize")
    
    return redirect('/')

@app.route('/download')
def dl_img():

    if len(os.listdir(colorized_dir)) > 1:
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for content in colorized_dir.iterdir():
                zf.write(content, content.name)

        stream.seek(0)

        os.remove(gs_dir)
        os.remove(eccv_dir)
        os.remove(siggraph_dir)
        can_dl = False

        return send_file(
            stream,
            as_attachment=True,
            attachment_filename='colorized.zip'
        )
    else:
        flash("No files to download")
        return redirect('/')


if __name__ == "__main__":
    app.run(threaded=True)