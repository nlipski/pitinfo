#APPLICATION_CONFIG="testing" python3 manage.py test tests/test_pit.py

from app.mod_pit.models import * # models is the db
from app.mod_pit.controllers import * #controllers are the connecting logic between the front-end and back-end
from datetime import date

def create_pit(database, name):
    pit = Pit_model(name = name)
    database.session.add(pit)
    database.session.commit()

def create_material(database, name):
    material = Material_model(name = name)
    database.session.add(material)
    database.session.commit()

def create_oxidation(database, name):
    oxidation = Oxidation_model(name = name)
    database.session.add(oxidation)
    database.session.commit()

def create_location(database, name, pit, stage, rl, blast = "", block = "", flitch = ""):
    #do nothing
    #locationop name is not needed. delete in the db 
    location = Location_openpit_model(name = name, pit = pit, stage = stage,
                        rl = rl, blast = blast,
                        block = block, flitch = flitch)
    database.session.add(location)
    database.session.commit()

def create_parcel(database, start, end, location_id, material_id, oxidation_id, bcm_undiluted, bcm_diluted, tonnes_undiluted, tonnes_diluted):
    parcel = Parcel_model(start = start, end = end, location_id = location_id, material_id = material_id, oxidation_id = oxidation_id, bcm_undiluted = bcm_undiluted, bcm_diluted = bcm_diluted, tonnes_undiluted = tonnes_undiluted, tonnes_diluted = tonnes_diluted)
    database.session.add(parcel)
    database.session.commit()

def create_grade(database, eval_type, analyte, grade, parcel_id):
    grade = Grade_model(eval_type = eval_type, analyte = analyte, grade = grade, diluted = grade, parcel_id = parcel_id)
    database.session.add(grade)
    database.session.commit()  

def create_stockpile(database, name, ore, rom):
    stockpile = Stockpile_model(name = name, ore = ore, rom = rom)
    database.session.add(stockpile)
    database.session.commit()

def create_plantclass(database, name):
    stockpile = Stockpile_model(name = name, active = True)
    database.session.add(Plant_class_model)
    database.session.commit()

def create_planttype(database, name):
    stockpile = Stockpile_model(name = name, active = True)
    database.session.add(Plant_type_model)
    database.session.commit()

def create_plant(database = "", name = "", active = True, start = date.today() ,retired = "", planttype_id=""):
    plant = Plant_model(name = name, active = active, start = start, retired = retired, planttype_id = planttype_id)
    database.session.add(Plant_model)
    database.session.commit()

def create_truckfactor(database, name, factor, planttype_id, oxidation_id): #need to add material type to the truck factor inputs
    truckfactor = Truck_factor_model(name = name, factor = factor, planttype_id = planttype_id, oxidation_id = oxidation_id)
    database.session.add(Truck_factor_model)
    database.session.commit()

def create_loadhaul(database, start, end, movementtype, loads, source, destination, comments = ""):
    loadhaul = Loadhaul_model(start= start, end = end, movementtype = movementtype, loads = loads, comments = comments, bcm = 0.0, tonnes = 0.0, ounces = 0.0)
    database.session.add(Loadhaul_model)
    database.session.commit()

def test__parcel_oz(database):
    #this test will
        #- create a pit, location
        #- create a parcel
        #- create a grade
        #- calculate the oz in that parcel
    
    #create the pit
    create_pit(database, name = "Test Pit 1")
    pit = Pit_model.query.first()

    #create the location
    name = "test name"
    location_pit = pit.id
    stage = "test_stage"
    rl = "test rl"
    blast = "test blast"
    block = "test block"
    flitch = ""
    create_location(database, name = name, pit = location_pit, stage = stage, rl = rl, blast = blast, block = block)    
    
    #create the material and oxidation
    name = "test material"
    create_material(name = name)
    material = Material_model.query.first()
    name = "test oxidation"
    create_oxidation(name = name)
    oxidation = Oxidation_model.query.first()

    sg = 2.60
    bcm_undiluted = 10000
    bcm_diluted = 9000
    tonnes_undiluted = 3500
    tonnes_diluted = 3200

    create_parcel(database, start= date.today(), end = date.today(),sg = sg, material_id=material.id, oxidation_id=oxidation.id, bcm_diluted= bcm_diluted, bcm_undiluted= bcm_undiluted, tonnes_diluted=tonnes_diluted, tonnes_undiluted= tonnes_undiluted)
    parcel = Parcel_model.query.first()

    eval_type="Grade Control"
    analyte = "Au"
    grade = 2.50

    create_grade(database,eval_type= eval_type, analyte = analyte, grade =grade, parcel_id= parcel.id)

    ###make sure this one works!!
    parcel_grade = Grade_model.query.filter_by(id = parcel.id).first()


def test__create_stockpile(database):
    name = "Test stockpile"
    create_stockpile(database, name = name, ore = True, rom = True)    
    stockpile = Stockpile_model.query.first()
    
    rows = database.session.query(Stockpile_model).count() #count the number of rows

    assert rows == 1
    assert stockpile.name == name
    assert stockpile.ore == True
    assert stockpile.rom == True
    
def test__create_location(database):
    create_pit(database, name = "Test Pit 1")    
    pit = Pit_model.query.first()
    
    name = "test name"
    location_pit = pit.id
    stage = "test_stage"
    rl = "test rl"
    blast = "test blast"
    block = "test block"
    flitch = ""

    create_location(database, name = name, pit = location_pit, stage = stage, rl = rl, blast = blast, block = block)
    
    rows = database.session.query(Location_openpit_model).count() #count the number of rows
    
    location = Location_openpit_model.query.first()
    
    assert rows == 1
    assert location.name == name
    assert location.pit == location_pit
    assert location.stage == stage
    assert location.rl == rl
    assert location.blast == blast
    assert location.block == block
    assert location.flitch == flitch

def test__create_pit(database):
    name = "Pit 1"

    #call the create_pit function 
    create_pit(database, name)
    database.session.commit()

    pit = Pit_model.query.first() #pull the first database entry
    rows = database.session.query(Pit_model).count() #count the number of rows

    assert pit.name == name
    assert rows ==1
    assert pit.id == 1

def test__delete_pit(database):
    #this test will:
        #- create a pit
        #- create locations assigned to the created pit
        #- delete the pit
        #- test that the associated locations have also been deleted
    pit_name = "test pit name"
    create_pit(database, name = pit_name)
    pit = Pit_model.query.first()

    name = "test name"
    location_pit = pit.id
    stage = "test_stage"
    rl = "test rl"
    blast = "test blast"
    block = "test block"
    flitch = ""

    num_of_locations = 10

    for i in range(num_of_locations):
        create_location(database, name = name + str(i), pit = location_pit, stage = stage + str(i), rl = rl + str(i), blast = blast + str(i), block = block + str(i))

    rows = database.session.query(Location_openpit_model).count() #count the number of rows 

    assert rows == num_of_locations

    database.session.delete(pit)
    database.session.commit()

    rows = database.session.query(Location_openpit_model).count() #count the number of rows 

    assert database.session.query(Location_openpit_model).count() == 0
    assert database.session.query(Pit_model).count() == 0