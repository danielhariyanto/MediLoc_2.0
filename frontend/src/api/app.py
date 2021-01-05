from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import algorithm
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # three forward slashes for relative path (no need to specify an exact location)
db = SQLAlchemy(app)

class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # references id (of type Integer) of each village entry
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    population = db.Column(db.Integer)
    assigned_center = db.Column(db.Integer)

    def __repr__(self):
        """returns a string every time we create a new element using village's id"""
        return '<Village %r>' % self.id
    
    def serialize(self):
       return {
           "id": self.id,
           "coordinates": [
               self.longitude,
               self.latitude
            ],
           "population": self.population,
           "assigned_center": self.assigned_center
       }
    

class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colorID = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    manpower = db.Column(db.Integer)

    def __repr__(self):
        return '<Center %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """routes to main to-do-list page, which accepts two methods: POST and GET"""
    if request.method == 'POST':
        village_coordinatesLong = request.form['coordinatesLong']
        village_coordinatesLat = request.form['coordinatesLat']
        village_pop = request.form['population']
        new_village = Village(longitude=village_coordinatesLong, latitude=village_coordinatesLat, population=village_pop, assigned_center=None)

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
        centerpass = [l for l in db.session.query(Village.assigned_center)]
        print([i.serialize() for i in Village.query.all()])
        return render_template('index.html', longitudespass=longitudespass, latitudespass=latitudespass, populationpass=populationpass, centerpass=centerpass)

@app.route('/database', methods=['GET'])
def showdb():
    villages = Village.query.order_by(Village.assigned_center).all()  # looks at database contents in order of date created and returns all of them
    return render_template('database.html', villages=villages)

@app.route('/delete/<int:id>')  # uses unique id to delete village
def delete(id):
    """removes village from database by unique id"""
    village_to_delete = Village.query.get_or_404(id)  # attempts to get village by id; if id does not exist, will display 404

    try:
        db.session.delete(village_to_delete)
        db.session.commit()  # deletes village from database
        return redirect('/database')  # after deletion, redirect back to homepage
    except:
        return 'There was an issue deleting your village'  # if there ever is a complication, this String will be returned


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """updates String content of specific village from database using submitted form"""
    village = Village.query.get_or_404(id)  # attempts to get village by id; if id does not exist, will display 404

    if request.method == 'POST':
        village.population = request.form['population']

        try:
            db.session.commit()  # no need to add or delete, just commit the updated content
            return redirect('/database')  # after update, redirect back to homepage to see updated village
        except:
            return 'There was an issue updating your village'  # if there ever is a complication, this String will be returned

    else:
        return render_template('update.html', village=village)


@app.route('/run', methods=['GET', 'POST'])
def run_algorithm():
    if request.method == 'POST':
        CENTROIDS = int(request.form['centroids'])
        MANPOWER = int(request.form['manpower'])

        ID = [i for (i, ) in db.session.query(Village.id).all()]
        XCOORDINATES = [i for (i, ) in db.session.query(Village.longitude).all()]
        YCOORDINATES = [i for (i, ) in db.session.query(Village.latitude).all()]
        POPULATION = [i for (i, ) in db.session.query(Village.population).all()]

        VILLAGES, CENTERS = algorithm.run(ID, XCOORDINATES, YCOORDINATES, POPULATION, CENTROIDS, MANPOWER)

        for i in range(len(ID)):
            village = Village.query.get_or_404(int(VILLAGES['id'][i]))
            village.assigned_center = int(VILLAGES['colorID'][i])


        # delete existing centers from previous runs
        try:
            db.session.query(Center).delete()
            db.session.commit()
        except:
            return 'There was an issue deleting your village'

        for i in range(len(CENTERS['colorID'])):
            new_center = Center(colorID=int(CENTERS['colorID'][i]), longitude=CENTERS['x'][i], latitude=CENTERS['y'][i], manpower=int(CENTERS['manpower'][i]))
            try:
                db.session.add(new_center)
            except:
                'oops'

        try:
            db.session.commit()
            return redirect('/database') #CHANGE TO HOMEPAGE
        except:
            return 'There was an issue running the algorithm'
        
    else:
        return render_template('run.html')

@app.route('/database2', methods=['GET'])
def showdb2():
    centers = Center.query.order_by(Center.colorID).all()  # looks at database contents in order of date created and returns all of them
    return render_template('database2.html', centers=centers)


if __name__ == "__main__":
    app.run(debug=True)
