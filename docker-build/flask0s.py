from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import os

us=os.getenv("MYSQL_USER")
pas=os.getenv("MYSQL_PASSWORD")
mdb=os.getenv("MYSQL_DB")

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+str(us)+":"+str(pas)+"@172.19.0.2:3306/"+str(mdb)
app.config['SQLALCHEMY_TRAK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class AteneiModel(db.Model):
    __tablename__="Atenei"
    idAteneo = db.Column(db.Integer(), primary_key=True)
    NomeAteneo=db.Column(db.String(60), nullable=False)
    Citta=db.Column(db.String(45), nullable=False)
    Regione=db.Column(db.String(45), nullable=False)

class CorsiModel(db.Model):
    __tablename__="Corsi"
    idCorso=db.Column(db.String(40),primary_key=True)
    NomeCorso=db.Column(db.String(200), nullable=False)

class LaureatiPerAnnoModel(db.Model):
    __tablename__="LaureatiPerAnno"
    Anno=db.Column(db.Integer(), primary_key=True)
    NumLaureti=db.Column(db.Integer(), nullable=False)
    idAteneo=db.Column(db.Integer(), db.ForeignKey("Atenei.idAteneo"), primary_key=True)
    idCorso=db.Column(db.String(10), db.ForeignKey("Corsi.idCorso"), primary_key=True)
    ateneo=db.relationship("AteneiModel")
    corso=db.relationship("CorsiModel")

resource_fields_atenei = { #devi crearlo in modo da restituire dati serializzati in json
    'idAteneo' : fields.Integer,
    'idCorso' : fields.List(fields.String)
}
resource_fields_corsi = { #devi crearlo in modo da restituire dati serializzati in json
    'idCorso' : fields.String,
    'idAteneo' : fields.List(fields.Integer)
}
resource_fields_lau = { #devi crearlo in modo da restituire dati serializzati in json
    'Anno' : fields.Integer,
    'NumLaureti' : fields.Integer,
    'Regione' : fields.String,
    'idCorso' : fields.String
}

class Corsi(Resource): #per utilizzare flask restful (Resource) utilizza l'http per interrogare ... il db
    #@marshal_with(resource_fields_atenei) #un decoratore per serislizzare un oggetto in json  ((quanto fai return user  lo serializza in json))
    def get(self, idCorso): #user_id  il numero passato nell'Url
        a=idCorso
        user=LaureatiPerAnnoModel.query.filter_by(idCorso = a).all() #prendi dalal tabella UserModel, l'user che ha id = user_id passato ala funzione
        l=[]
        for u in user:
            l.append(u.idAteneo)
        if not user:
            abort(404, message = "User Not Found") #invia questo messaggio se non trova niente
        return {
            'idCorso' : idCorso,
            'idAteneo' : l
            } #se lo trovi devi restituirlo in JSON (serializzabile)

class Atenei(Resource): #per utilizzare flask restful (Resource) utilizza l'http per interrogare ... il db
    @marshal_with(resource_fields_atenei) #un decoratore per serislizzare un oggetto in json  ((quanto fai return user  lo serializza in json))
    def get(self, idAteneo): #user_id  il numero passato nell'Url
        user=LaureatiPerAnnoModel.query.filter_by(idAteneo = idAteneo).all() #prendi dalal tabella UserModel, l'user che ha id = user_id passato ala funzione
        l=[]
        for u in user:
            l.append(u.idCorso)
        if not user:
            abort(404, message = "User Not Found") #invia questo messaggio se non trova niente
        return {
            'idAteneo' : idAteneo,
            'idCorso' : l
            } #se lo trovi devi restituirlo in JSON (serializzabile)

class LaureatiPerAnno(Resource): #per utilizzare flask restful (Resource) utilizza l'http per interrogare ... il db
    @marshal_with(resource_fields_lau) #un decoratore per serislizzare un oggetto in json  ((quanto fai return user  lo serializza in json))
    def get(self, Anno): #user_id  il numero passato nell'Url
        args = parser.parse_args()
        print(args["idCorso"] )
        if args["idCorso"] and args["Regione"]:
            z=0
            try: 
                a=int(args["idCorso"])
            except:
                a=args["idCorso"]
            user=AteneiModel.query.filter_by(Regione = args["Regione"]).all()
            for at in user:
                print(at.idAteneo)
                i=LaureatiPerAnnoModel.query.filter_by(Anno = int(Anno), idAteneo = at.idAteneo, idCorso=a).all()
                print(i)
                for laureato in i:
                    print(laureato.NumLaureti)
                    z+=laureato.NumLaureti
            return { 
                'Anno' : Anno,
                'NumLaureti' : z,
                'Regione' : args["Regione"],
                'idCorso' : args["idCorso"]
            }
        elif args["idCorso"]:
            user=LaureatiPerAnnoModel.query.filter_by(Anno = int(Anno), idCorso = args["idCorso"]).all() 
        elif args["Regione"]:
            print("OK")
            z=0
            user=AteneiModel.query.filter_by(Regione = args["Regione"]).all()

            for at in user:
                i=LaureatiPerAnnoModel.query.filter_by(Anno = int(Anno), idAteneo = at.idAteneo).all()
                for laureato in i:
                    z+=laureato.NumLaureti
            return { 
                'Anno' : Anno,
                'NumLaureti' : z,
                'Regione' : args["Regione"],
                'idCorso' : args["idCorso"]
            }
        else:
            user=LaureatiPerAnnoModel.query.filter_by(Anno = int(Anno)).all() #prendi dalal tabella UserModel, l'user che ha id = user_id passato ala funzione
        if not user:
            abort(404, message = "User Not Found") #invia questo messaggio se non trova niente
        i=0
        for u in user:
            i+=u.NumLaureti
        return { 
                'Anno' : Anno,
                'NumLaureti' : i,
                'Regione' : args["Regione"],
                'idCorso' : args["idCorso"]
            }

parser = reqparse.RequestParser()
parser.add_argument('idCorso', type=str, required=False)
parser.add_argument('Regione', type=str, required=False)
api.add_resource(Corsi, "/corsi/<string:idCorso>")
api.add_resource(Atenei, "/atenei/<int:idAteneo>")
api.add_resource(LaureatiPerAnno, "/laureati/<string:Anno>")  

if __name__=="__main__":
    app.run(host="0.0.0.0") #debugga
