# Iniciando o servidor
FLASK_ENV=development FLASK_APP=app.py /opt/conda/bin/python -m flask run --host=0.0.0.0

# Executando para inserir no banco
/opt/conda/bin/python manage.py insert_database --classes "images/flickr.names" --boundingboxes "images/flickr.txt"
/opt/conda/bin/python manage.py insert_database --classes "images/LogosInTheWild-v2.names" --boundingboxes "images/LogosInTheWild-v2.txt"