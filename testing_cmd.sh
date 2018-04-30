NOWPWD=${PWD}
export FLASK_APP=app/compdb/compdb.py
#flask init_db
ln -s $NOWPWD/components.db /tmp/components.db
flask run --host=0.0.0.0 --port=8080
