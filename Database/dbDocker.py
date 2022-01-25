import csv, sys
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql+pymysql://root:<METTI PASSWORD>@192.168.43.53:3306/laureati2')
connection = engine.connect()
Session=sessionmaker(bind=engine)
session = Session()
Base=declarative_base()

class Atenei(Base):
    __tablename__="Atenei"
    idAteneo = Column(Integer(), primary_key=True)
    NomeAteneo=Column(String(60), nullable=False)
    Citta=Column(String(45), nullable=False)
    Regione=Column(String(45), nullable=False)

class Corsi(Base):
    __tablename__="Corsi"
    idCorso=Column(String(40),primary_key=True)
    NomeCorso=Column(String(200), nullable=False)

class LaureatiPerAnno(Base):
    __tablename__="LaureatiPerAnno"
    Anno=Column(Integer(), primary_key=True)
    NumLaureti=Column(Integer(), nullable=False)
    idAteneo=Column(Integer(), ForeignKey("Atenei.idAteneo"), primary_key=True)
    idCorso=Column(String(10), ForeignKey("Corsi.idCorso"), primary_key=True)
    ateneo=relationship("Atenei")
    corso=relationship("Corsi")
#Base.metadata.create_all(engine)

toup=[]
with open("LaureatiCorsiAtenei", newline='') as csvfile:
    reader=csv.reader(csvfile)
    i=0
    for row in reader:
        if i != 0:
            #if (row[1],row[2],row[4]) not in toup: #LaureatiPerAnno
            #if row[2] not in toup: #Atenei
            #if row[4] not in toup: #Corsi
                #l=LaureatiPerAnno(Anno=int(row[1]), NumLaureti=int(row[8]), idAteneo=int(row[2]), idCorso=row[4])
                #l=Atenei(idAteneo=row[2], NomeAteneo=row[3], Citta=row[6], Regione=row[7])
                #l=Corsi(idCorso=row[4], NomeCorso=row[5])
                #toup.append((row[1],row[2],row[4])) #laureatiPerAnno
                #toup.append(row[2]) #Atenei
                #toup.append(row[4]) #Corsi               
                session.add(l)
        i+=1
    session.commit()