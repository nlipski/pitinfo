#APPLICATION_CONFIG="testing" python3 manage.py test tests/test_pit.py

from app.mod_pit.models import * # models is the db
from app.mod_pit.controllers import * #controllers are the connecting logic between the front-end and back-end

def create_pit(database, name):
    pit = Pit_model(name = name)
    database.session.add(pit)
    database.session.commit()

def create_location(database, name, pit, stage, rl, blast = "", block = "", flitch = ""):
    #do nothing
    #locationop name is not needed. delete in the db 
    location = Location_openpit_model(name = name, pit = pit, stage = stage,
                        rl = rl, blast = blast,
                        block = block, flitch = flitch)
    database.session.add(location)
    database.session.commit()

def create_stockpile(database, name, ore, rom):
    stockpile = Stockpile_model(name = name, ore = ore, rom = rom)
    database.session.add(stockpile)
    database.session.commit()

def test__create_stockpile(database):
    name = "Test stockpile"
    create_stockpile(database, name = name, ore = True, rom = True)    
    stockpile = Stockpile_model.query.first()
    
    rows = database.session.query(Location_openpit_model).count() #count the number of rows

    assert rows == 1
    assert location.name == name
    assert location.pit == location_pit
    assert location.stage == stage
    assert location.rl == rl
    assert location.blast == blast
    assert location.block == block
    assert location.flitch == flitch

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
    
    #... still need to write.
    
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
    pit = Pit.query.first()

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