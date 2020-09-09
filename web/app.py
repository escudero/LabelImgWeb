from flask import Flask, send_file, render_template, jsonify, request
import json
import os
import helpers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:example@db/LabelImgWeb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

helpers.init_app(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/image/<path:name>')
def image(name):
  filename = os.path.join('images', name)
  print(filename)
  if not os.path.isfile(filename):
    filename = ''
  return send_file(filename)

@app.route('/image_next')
def next_image():
  direction = request.args.get('direction') 
  image_id = request.args.get('image_id')
  img, bblist = helpers.get_next_image_and_boundingboxes(image_id, direction)
  values = {
    'image': img.filename.replace('images/', '/image/'),
    'image_id': img.id,
    'boundingboxes': [
      {'class_name': bb.class_name, 'top': bb.top, 'left': bb.left, 'width': bb.width, 'height': bb.height}
      for bb in bblist
    ]
  }
  return jsonify(values)

@app.route('/save', methods=['POST'])
def save():
  data = json.loads(request.form.get('data'))
  image_id = int(data['image_id'])
  boundingboxes = data['boundingboxes']
  ret = helpers.remove_and_insert_boundingboxes(image_id, boundingboxes)
  return jsonify({'ret': ret})