from flask_script import Manager

import app

manager = Manager(app.app)

@manager.option('-c', '--classes', help='File classes Names')
@manager.option('-b', '--boundingboxes', help='File Bounding Boxes')
def insert_database(classes, boundingboxes):
  with open(classes) as f:
    classes_list = [s.strip() for s in f.readlines()]
  print(classes_list)
  with open(boundingboxes, "r") as f:
      while True:
          line = f.readline().strip()
          if line == '' or line is None:
              break
          filename, coords = line.split(' ', 1)
          exists_image = app.helpers.check_exists_image(filename)
          if not exists_image:
            img = app.helpers.insert_image(filename)
            print(f'>>>> {img.id}')
            app.helpers.remove_boundingboxes_from_image(img)
            for coord in coords.split(' '):
                coord = [int(i) for i in coord.split(',')]
                left = coord[0]
                top = coord[1]
                width = coord[2] - left
                height = coord[3] - top
                class_name = classes_list[coord[4]]
                app.helpers.insert_boundingbox(img, class_name, top, left, width, height)

if __name__ == "__main__":
    manager.run()
