from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # three forward slashes for relative path (no need to specify an exact location)
db = SQLAlchemy(app)

class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # references id (of type Integer) of each village entry
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    population = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """returns a string every time we create a new element using village's id"""
        return '<Village %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """routes to main to-do-list page, which accepts two methods: POST and GET"""
    if request.method == 'POST':
        village_coordinatesLong = request.form['coordinatesLong']
        village_coordinatesLat = request.form['coordinatesLat']
        village_pop = request.form['population']
        new_village = Village(longitude=village_coordinatesLong, latitude=village_coordinatesLat, population=village_pop)

        try:
            db.session.add(new_village)
            db.session.commit()  # adds village entry to database
            return redirect('/')  # after update, redirect back to homepage to see new village
        except:
            return 'There was an issue adding your village'  # if there ever is a complication, this String will be returned

    else:
        longitudespass = [i for i in db.session.query(Village.longitude)]
        latitudespass = [j for j in db.session.query(Village.latitude)]
        populationpass = [k for k in db.session.query(Village.population)]
        return render_template('index.html', longitudespass=longitudespass, latitudespass=latitudespass, populationpass=populationpass)

@app.route('/database', methods=['GET'])
def showdb():
    villages = Village.query.order_by(Village.date_created).all()  # looks at database contents in order of date created and returns all of them
    return render_template('database.html', villages=villages)

@app.route('/delete/<int:id>')  # uses unique id to delete village
def delete(id):
    """removes village from database by unique id"""
    village_to_delete = Village.query.get_or_404(id)  # attempts to get village by id; if id does not exist, will display 404

    try:
        db.session.delete(village_to_delete)
        db.session.commit()  # deletes village from database
        return redirect('/')  # after deletion, redirect back to homepage
    except:
        return 'There was an issue deleting your village'  # if there ever is a complication, this String will be returned


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """updates String content of specific village from database using submitted form"""
    village = Village.query.get_or_404(id)  # attempts to get village by id; if id does not exist, will display 404

    if request.method == 'POST':
        village.longitude = request.form['coordinatesLong']
        village.latitude = request.form['coordinatesLat']
        village.population = request.form['population']

        try:
            db.session.commit()  # no need to add or delete, just commit the updated content
            return redirect('/database')  # after update, redirect back to homepage to see updated village
        except:
            return 'There was an issue updating your village'  # if there ever is a complication, this String will be returned

    else:
        return render_template('update.html', village=village)


if __name__ == "__main__":
    app.run(debug=True)
