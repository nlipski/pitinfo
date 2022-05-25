# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models import db

from datetime import datetime

Base = declarative_base()
metadata = Base.metadata


class Activitytype(db.Model):
    __tablename__ = 'activitytype'

    id = Column(Integer, primary_key=True, comment='Types of activities: load and haul, drilling, blasting.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Company(db.Model):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Consclas(db.Model):
    __tablename__ = 'consclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Department(db.Model):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Dwnclas(db.Model):
    __tablename__ = 'dwnclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Firingtype(db.Model):
    __tablename__ = 'firingtype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Locationug(db.Model):
    __tablename__ = 'locationug'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
    loctype_id = Column(Integer, nullable=False)
    detail1 = Column(String(45), nullable=False)
    detail2 = Column(String(45))
    detail3 = Column(String(45))
    detail4 = Column(String(45))
    detail5 = Column(String(45))
    detail6 = Column(String(45))
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Material(db.Model):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, comment='The grade categorization for ore and waste.')
    name = Column(String(45), nullable=False, comment='Grade bins. ')
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Measure(db.Model):
    __tablename__ = 'measure'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(String(150), nullable=False)
    unit = Column(String(45), nullable=False)
    type = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    measure_col = Column(String(45))


class Oxidation(db.Model):
    __tablename__ = 'oxidation'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Pit(db.Model):
    __tablename__ = 'pit'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    pit = Column(String(45), nullable=False)


class Plantclas(db.Model):
    __tablename__ = 'plantclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Stockpile(db.Model):
    __tablename__ = 'stockpile'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    ore = Column(TINYINT, nullable=False, comment='is it an ore stockpile or a waste dump?')
    rom = Column(TINYINT, nullable=False, comment='is the stockpile on the ROM or not?')


class Constype(db.Model):
    __tablename__ = 'constype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    consclass_id = Column(ForeignKey('consclass.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    consclass = relationship('Consclas')


class Dwntype(db.Model):
    __tablename__ = 'dwntype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    stand = Column(TINYINT, nullable=False)
    maintenance = Column(TINYINT, nullable=False)
    planned = Column(TINYINT, nullable=False)
    ops = Column(TINYINT, nullable=False)
    dwnclass_id = Column(ForeignKey('dwnclass.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    dwnclass = relationship('Dwnclas')


class Locationop(db.Model):
    __tablename__ = 'locationop'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    pit = Column(ForeignKey('pit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    stage = Column(String(45), nullable=False)
    rl = Column(String(45), nullable=False)
    blast = Column(String(45))
    block = Column(String(45))
    flitch = Column(String(45))

    pit1 = relationship('Pit')


class Person(db.Model):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    login = Column(String(45), nullable=False)
    employee_number = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    company_id = Column(ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    company = relationship('Company')


class Planttype(db.Model):
    __tablename__ = 'planttype'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    plantclass_id = Column(ForeignKey('plantclass.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    plantclass = relationship('Plantclas')


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    shift_boss = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    department_id = Column(ForeignKey('department.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    department = relationship('Department')


class Budget(db.Model):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    budget_col = Column(String(45), nullable=False)
    volume = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    metal = Column(DECIMAL(10, 0), nullable=False)
    drillm = Column(DECIMAL(10, 0))
    lhrate = Column(DECIMAL(10, 0))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    comment = Column(String(45))
    stockpile_id = Column(ForeignKey('stockpile.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    locationop_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    oxidation_id = Column(ForeignKey('oxidation.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    material_id = Column(ForeignKey('material.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    locationop = relationship('Locationop')
    material = relationship('Material')
    oxidation = relationship('Oxidation')
    stockpile = relationship('Stockpile')


class Consumable(db.Model):
    __tablename__ = 'consumable'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    supplier = Column(String(45))
    explosive = Column(TINYINT, nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    constype_id = Column(ForeignKey('constype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    constype = relationship('Constype')


class Parcel(db.Model):
    __tablename__ = 'parcel'

    id = Column(Integer, primary_key=True, comment='Parcel is a dig block in the open pit setting.')
    sg = Column(DECIMAL(10, 0), nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)
    location_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    material_id = Column(ForeignKey('material.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    oxidation_id = Column(ForeignKey('oxidation.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    evaluations_id = Column(Integer, nullable=False)

    location = relationship('Locationop')
    material = relationship('Material')
    oxidation = relationship('Oxidation')


class Plant(db.Model):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(TINYINT, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    start = Column(DateTime, nullable=False)
    retired = Column(DateTime)
    planttype_id = Column(ForeignKey('planttype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    planttype = relationship('Planttype')


class Rolehist(db.Model):
    __tablename__ = 'rolehist'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    role_id = Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    person_id = Column(ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    person = relationship('Person')
    role = relationship('Role')


class Shiftactivity(db.Model):
    __tablename__ = 'shiftactivity'

    id = Column(Integer, primary_key=True, comment='The truck counts table.')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comments = Column(String(45))
    shiftboss = Column(ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    activity_id = Column(ForeignKey('activitytype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    pit_id = Column(ForeignKey('pit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    supervisor = Column(ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    activity = relationship('Activitytype')
    pit = relationship('Pit')
    person = relationship('Person', primaryjoin='Shiftactivity.shiftboss == Person.id')
    person1 = relationship('Person', primaryjoin='Shiftactivity.supervisor == Person.id')


class Survey(db.Model):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    volume = Column(DECIMAL(10, 0), nullable=False)
    location_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    location = relationship('Locationop')


class Truckfactor(db.Model):
    __tablename__ = 'truckfactor'

    id = Column(Integer, primary_key=True, comment='Types of activities: load and haul, drilling, blasting.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    factor = Column(DECIMAL(10, 0), nullable=False)
    planttype_id = Column(ForeignKey('planttype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    planttype = relationship('Planttype')


class Brokenstock(db.Model):
    __tablename__ = 'brokenstock'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')
    date = Column(DateTime, nullable=False)
    bcm = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comment = Column(String(45))
    ounces = Column(DECIMAL(10, 0), nullable=False)
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    parcel = relationship('Parcel')


class Downtime(db.Model):
    __tablename__ = 'downtime'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    usable = Column(TINYINT, nullable=False)
    dwntype_id = Column(ForeignKey('dwntype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    plant_id = Column(ForeignKey('plant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    dwntype = relationship('Dwntype')
    location = relationship('Locationop')
    plant = relationship('Plant')


class Drilling(db.Model):
    __tablename__ = 'drilling'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    hole_number = Column(Integer, nullable=False)
    hole_length = Column(DECIMAL(10, 0), nullable=False)
    hole_diameter = Column(DECIMAL(10, 0), nullable=False)
    azimuth = Column(Integer, nullable=False)
    dip = Column(Integer)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comment = Column(String(45))
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    redrill = Column(TINYINT, nullable=False, server_default=text("'0'"))
    drilling_col = Column(String(45))
    patternid = Column(String(45))

    parcel = relationship('Parcel')


class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    type = Column(String(45), nullable=False)
    preferred = Column(TINYINT, nullable=False, server_default=text("'1'"))
    bcm_undiluted = Column(DECIMAL(10, 0), nullable=False)
    bcm_diluted = Column(DECIMAL(10, 0), nullable=False)
    tonnes_undiluted = Column(DECIMAL(10, 0), nullable=False)
    tonnes_diluted = Column(DECIMAL(10, 0), nullable=False)
    moisture = Column(DECIMAL(10, 0))
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    parcel = relationship('Parcel')


class Grade(db.Model):
    __tablename__ = 'grade'

    id = Column(Integer, primary_key=True, comment='The grades for each parcel (dig block). Many-to-1 because you could be analyzing for multiple metals.\\n\\nDiluted grade is calculated off of the truck counts (over mining). Do some sites have dilution in the block model?')
    eval_type = Column(String(45))
    analyte = Column(String(45), nullable=False)
    grade = Column(DECIMAL(10, 0), nullable=False)
    diluted = Column(DECIMAL(10, 0), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    parcel = relationship('Parcel')


class Loadhaul(db.Model):
    __tablename__ = 'loadhaul'

    id = Column(Integer, primary_key=True, comment='The truck counts table.')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    movementtype = Column(Integer, nullable=False, server_default=text("'0'"), comment='crusher feed, haulage, rehandle, etc.')
    loads = Column(Integer, nullable=False)
    comments = Column(String(45))
    bcm = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    ounces = Column(DECIMAL(10, 0), nullable=False)
    source = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='Source.')
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    destination = Column(ForeignKey('stockpile.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    stockpile = relationship('Stockpile')
    parcel = relationship('Parcel')
    planthours = relationship('Planthour', secondary='planthour_has_loadhaul')


class Firing(db.Model):
    __tablename__ = 'firing'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    meters_adv = Column(DECIMAL(10, 0), nullable=False)
    holes_fired = Column(Integer, nullable=False)
    maters_adv_adj = Column(DECIMAL(10, 0), nullable=False)
    tonnes_fired = Column(DECIMAL(10, 0), nullable=False)
    bcm_fired = Column(DECIMAL(10, 0), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comment = Column(String(45))
    firingtype_id = Column(ForeignKey('firingtype.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    drilling_id = Column(ForeignKey('drilling.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    benchheight = Column(DECIMAL(10, 0))
    burden = Column(DECIMAL(10, 0))
    spacing = Column(DECIMAL(10, 0))
    subdrill = Column(DECIMAL(10, 0))

    drilling = relationship('Drilling')
    firingtype = relationship('Firingtype')
    location = relationship('Locationop')


class Stockpilebalance(db.Model):
    __tablename__ = 'stockpilebalance'

    id = Column(Integer, primary_key=True)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    adjtonnes = Column(DECIMAL(10, 0), nullable=False)
    ounces = Column(DECIMAL(10, 0), nullable=False)
    adjounces = Column(DECIMAL(10, 0), nullable=False)
    grade = Column(DECIMAL(10, 0), nullable=False)
    adjgrade = Column(DECIMAL(10, 0), nullable=False)
    loadhaul_id = Column(ForeignKey('loadhaul.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_id = Column(ForeignKey('locationop.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    loadhaul = relationship('Loadhaul')
    location = relationship('Locationop')


class Consfiring(db.Model):
    __tablename__ = 'consfiring'

    id = Column(Integer, primary_key=True)
    quantity = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    consumable_id = Column(ForeignKey('consumable.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    consumable = relationship('Consumable')
    firing = relationship('Firing')


class Measfiring(db.Model):
    __tablename__ = 'measfiring'

    id = Column(Integer, primary_key=True)
    quantity = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    measure_id = Column(ForeignKey('measure.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    firing = relationship('Firing')
    measure = relationship('Measure')


class Planthour(db.Model):
    __tablename__ = 'planthour'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    starthour = Column(DECIMAL(10, 0), nullable=False)
    endhour = Column(DECIMAL(10, 0), nullable=False)
    comment = Column(String(45))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    plant_id = Column(ForeignKey('plant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    drilling_id = Column(ForeignKey('drilling.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    person_id = Column(ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    shiftactivity_id = Column(ForeignKey('shiftactivity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    drilling = relationship('Drilling')
    firing = relationship('Firing')
    person = relationship('Person')
    plant = relationship('Plant')
    shiftactivity = relationship('Shiftactivity')


t_planthour_has_loadhaul = Table(
    'planthour_has_loadhaul', metadata,
    Column('planthour_id', ForeignKey('planthour.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('loadhaul_id', ForeignKey('loadhaul.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)
