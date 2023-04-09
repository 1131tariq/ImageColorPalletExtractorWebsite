from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images/"
app.secret_key = "GF7G8FU7G8F9CIB789CVDBUD78FX9BXZDD9CS8"
Bootstrap(app)


class ImageForm(FlaskForm):
    image = FileField("Upload Image", validators=[DataRequired()])
    colors = IntegerField("Number of colors", validators=[DataRequired()], default=10)
    submit = SubmitField("Get Colors")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ImageForm()
    if form.validate_on_submit():
        image = form.image.data
        color = form.colors.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for("colors", image=filename, colorcount= color))
    return render_template("index.html", form=form)


@app.route("/colors/<image>/<colorcount>")
def colors(image, colorcount):
    path = f"static/images/{image}"
    array = np.array(Image.open(path))
    colors, counts = np.unique(array.reshape(-1, array.shape[-1]), axis=0, return_counts=True)
    colorcount = int(colorcount)
    most_common_colors = colors[np.argsort(counts)][::-1][:colorcount]
    return render_template("colors.html", image=path, colors=most_common_colors)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
