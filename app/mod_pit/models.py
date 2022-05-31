# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Table, text, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models import db

from datetime import datetime

Base = declarative_base()
metadata = Base.metadata




class Consumable_model(db.Model):
    __tablename__ = 'consumable'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    supplier = Column(String(45))
    explosive = Column(Boolean, default= False, nullable=False)
    active = Column(Boolean, default= False, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    
    consumables_type_id = Column(ForeignKey('consumables_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    consumables_type = relationship('Consumables_type_model')


class Consumables_type_model(db.Model):
    __tablename__ = 'consumables_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    consumables_class_id = Column(ForeignKey('consumables_class.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    consumables_class = relationship('Consumables_class_model')


class Consumables_class_model(db.Model):
    __tablename__ = 'consumables_class'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())


class Department_model(db.Model):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())


class Activity_type_model(db.Model):
    __tablename__ = 'activity_type'

    id = Column(Integer, primary_key=True, comment='Types of activities: load and haul, drilling, blasting.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45), nullable=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))



class Downtime_class_model(db.Model):
    __tablename__ = 'dwnclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())

class Downtime_type_model(db.Model):
    __tablename__ = 'downtime_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
    stand = Column(Boolean, nullable=False)
    maintenance = Column(Boolean, nullable=False)
    planned = Column(Boolean, nullable=False)
    ops = Column(Boolean, nullable=False)
    dwnclass_id = Column(ForeignKey('dwnclass.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    dwnclass = relationship('Dwnclas')


class Downtime_model(db.Model):
    __tablename__ = 'downtime'

    id = Column(Integer, primary_key=True)

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    usable = Column(Boolean, nullable=False)

    comment = Column(String(45), nullable=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    downtime_type_id = Column(ForeignKey('downtime_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    downtime_type = relationship('Downtime_type_model')

    location_id = Column(ForeignKey('location_openpit.id', ondelete='CASCADE', onupdate='CASCADE'), index=True, nullable=True)
    location = relationship('Location_openpit_model')
   
    plant_id = Column(ForeignKey('plant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    plant = relationship('Plant_model')


class Firing_type_model(db.Model):
    __tablename__ = 'firing_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())

class Location_underground(db.Model):
    __tablename__ = 'location_underground'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')

    detail1 = Column(String(45), nullable=False)
    detail2 = Column(String(45), nullable=True)
    detail3 = Column(String(45), nullable=True)
    detail4 = Column(String(45), nullable=True)
    detail5 = Column(String(45), nullable=True)
    detail6 = Column(String(45), nullable=True)
    comment = Column(String(45), nullable=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())

class Location_openpit_model(db.Model):
    __tablename__ = 'location_openpit'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    comment = Column(String(45), nullable=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    
    stage = Column(String(45), nullable=False)
    rl = Column(String(45), nullable=False)
    blast = Column(String(45), nullable=True)
    block = Column(String(45), nullable=True)
    flitch = Column(String(45), nullable=True)

    pit_id = Column(ForeignKey('pit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    pit1 = relationship('Pit_model')


class Material_model(db.Model):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, comment='The grade categorization for ore and waste.')
    name = Column(String(45), nullable=False, comment='Grade bins. ')
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())


class Measure_model(db.Model):
    __tablename__ = 'measure'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(String(150), nullable=False)
    unit = Column(String(45), nullable=False)
    unit_type = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())


class Oxidation_model(db.Model):
    __tablename__ = 'oxidation'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())


class Pit_model(db.Model):
    __tablename__ = 'pit'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
<<<<<<< HEAD
    comment = Column(String(45))
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
=======
    comment = Column(String(45), nullable=True)

    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
>>>>>>> bbff0c7 ([mod_pit] - update DB)


class Plant_class_model(db.Model):
    __tablename__ = 'plant_class'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
<<<<<<< HEAD
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
=======
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
>>>>>>> bbff0c7 ([mod_pit] - update DB)


class Plant_type_model(db.Model):
    __tablename__ = 'plant_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    plant_class_id = Column(ForeignKey('plant_class.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    plant_class = relationship('Plant_class_model')


class Plant_model(db.Model):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    active = Column(Boolean, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    start = Column(DateTime, nullable=False)
    retired = Column(DateTime, nullable=True)
    
    plant_type_id = Column(ForeignKey('plant_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    plant_type = relationship('Plant_type_model')


class Plant_hour_model(db.Model):
    __tablename__ = 'plant_hour'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    # Measurement of the plant
    starthour = Column(DECIMAL(10, 0), nullable=False)
    endhour = Column(DECIMAL(10, 0), nullable=False)
    
    comment = Column(String(45), nullable=True)
    
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    drilling_id = Column(ForeignKey('drilling.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    drilling = relationship('Drilling_model')
    
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing = relationship('Firing_model')
    # TODO
    person_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    person = relationship('user_model')

    plant_id = Column(ForeignKey('plant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    plant = relationship('Plant_model')
    
    shift_activity_id = Column(ForeignKey('shift_activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    shift_activity = relationship('Shift_activity_model')


class Stockpile_model(db.Model):
    __tablename__ = 'stockpile'

    id = Column(Integer, primary_key=True, comment='The material source locations by pit, stage, RL, blast, block, flitch.')
    name = Column(String(45), nullable=False)
    
    comment = Column(String(45), nullable=True)
    
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    ore = Column(Boolean, nullable=False, comment='is it an ore stockpile or a waste dump?')
    rom = Column(Boolean, nullable=False, comment='is the stockpile on the ROM or not?')





class Budget_model(db.Model):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    volume = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    metal = Column(DECIMAL(10, 0), nullable=False)
    drill_meters = Column(DECIMAL(10, 0), nullable=True)
    loadhaul_rate = Column(DECIMAL(10, 0), nullable=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    comment = Column(String(45), nullable=True)
    stockpile_id = Column(ForeignKey('stockpile.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_openpit_id = Column(ForeignKey('location_openpit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    oxidation_id = Column(ForeignKey('oxidation.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    material_id = Column(ForeignKey('material.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    location_openpit = relationship('Location_openpit_model')
    material = relationship('Material_model')
    oxidation = relationship('Oxidation_model')
    stockpile = relationship('Stockpile_model')


class Parcel_model(db.Model):
    __tablename__ = 'parcel'

    id = Column(Integer, primary_key=True, comment='Parcel is a dig block in the open pit setting.')
    sg = Column(DECIMAL(10, 0), nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)

    bcm_undiluted = Column(DECIMAL(10, 0), nullable=False)
    bcm_diluted = Column(DECIMAL(10, 0), nullable=False)
    tonnes_undiluted = Column(DECIMAL(10, 0), nullable=False)
    tonnes_diluted = Column(DECIMAL(10, 0), nullable=False)
    moisture = Column(DECIMAL(10, 0), nullable=True)

    location_id = Column(ForeignKey('location_openpit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    material_id = Column(ForeignKey('material.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    oxidation_id = Column(ForeignKey('oxidation.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())

    location = relationship('Location_openpit_model')
    material = relationship('Material_model')
    oxidation = relationship('Oxidation_model')



class Shift_activity_model(db.Model):
    __tablename__ = 'shift_activity'

    id = Column(Integer, primary_key=True, comment='The truck counts table.')

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    comments = Column(String(45), nullable=True)

    shiftboss = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    supervisor = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    activity_id = Column(ForeignKey('activity_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    activity = relationship('Activity_type_model')

    pit_id = Column(ForeignKey('pit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    pit = relationship('Pit_model')

    person = relationship('user_model', primaryjoin='Shift_activity.shiftboss == user_model.id')
    person1 = relationship('user_model', primaryjoin='Shift_activity.supervisor == user_model.id')


class Survey_model(db.Model):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    volume = Column(DECIMAL(10, 0), nullable=False)

    location_id = Column(ForeignKey('location_openpit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location = relationship('Location_openpit_model')


class Truck_factor_model(db.Model):
    __tablename__ = 'truck_factor'

    id = Column(Integer, primary_key=True, comment='Types of activities: load and haul, drilling, blasting.')
    name = Column(String(45), nullable=False)
    comment = Column(String(45), nullable=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    factor = Column(DECIMAL(10, 0), nullable=False)
    
    plant_type_id = Column(ForeignKey('plant_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    plant_type = relationship('Plant_type_model')

    oxidation_id = Column(ForeignKey('oxidation.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    oxidation = relationship('Oxidation_model')






class Broken_stock_model(db.Model):
    __tablename__ = 'broken_stock'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')
    date = Column(DateTime, nullable=False)
    bcm = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    comment = Column(String(45), nullable=True)
    ounces = Column(DECIMAL(10, 0), nullable=False)
    
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    parcel = relationship('Parcel_model')




class Drilling_model(db.Model):
    __tablename__ = 'drilling'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    comment = Column(String(45), nullable=True)

    hole_number = Column(Integer, nullable=False)
    hole_length = Column(DECIMAL(10, 0), nullable=False)
    hole_diameter = Column(DECIMAL(10, 0), nullable=False)

    azimuth = Column(Integer, nullable=False)
    dip = Column(Integer, nullable=True)

    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    
    
    redrill = Column(Boolean, nullable=False, default=False)
    drill_pattern = Column(String(45), nullable=True)

    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    parcel = relationship('Parcel_model')


class Grade_model(db.Model):
    __tablename__ = 'grade'

    id = Column(Integer, primary_key=True, comment='The grades for each parcel (dig block). Many-to-1 because you could be analyzing for multiple metals.\\n\\nDiluted grade is calculated off of the truck counts (over mining). Do some sites have dilution in the block model?')
    eval_type = Column(String(45))
    analyte = Column(String(45), nullable=False)
    grade = Column(DECIMAL(10, 0), nullable=False)
    diluted = Column(DECIMAL(10, 0), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    parcel = relationship('Parcel_model')


class Loadhaul_model(db.Model):
    __tablename__ = 'loadhaul'

    id = Column(Integer, primary_key=True, comment='The truck counts table.')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    movementtype = Column(Integer, nullable=False, server_default=text("'0'"), comment='crusher feed, haulage, rehandle, etc.')
    loads = Column(Integer, nullable=False)
    comments = Column(String(45), nullable=True)
    bcm = Column(DECIMAL(10, 0), nullable=False)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    ounces = Column(DECIMAL(10, 0), nullable=False)
    
    parcel_id = Column(ForeignKey('parcel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='Source.')
    
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    stockpile_id = Column(ForeignKey('stockpile.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    stockpile = relationship('Stockpile_model')

    parcel = relationship('Parcel_model')
    plant_hours = relationship('Plant_hour_model', secondary='plant_hour_has_loadhaul')


class Firing_model(db.Model):
    __tablename__ = 'firing'

    id = Column(Integer, primary_key=True, comment='Do we need to add a depletion id?')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    meters_adv = Column(DECIMAL(10, 0), nullable=False)
    holes_fired = Column(Integer, nullable=False)
    maters_adv_adj = Column(DECIMAL(10, 0), nullable=False)
    tonnes_fired = Column(DECIMAL(10, 0), nullable=False)
    bcm_fired = Column(DECIMAL(10, 0), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    comment = Column(String(45), nullable=True)
    firing_type_id = Column(ForeignKey('firing_type.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_id = Column(ForeignKey('location_openpit.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    drilling_id = Column(ForeignKey('drilling.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    benchheight = Column(DECIMAL(10, 0), nullable=True)
    burden = Column(DECIMAL(10, 0), nullable=True)
    spacing = Column(DECIMAL(10, 0), nullable=True)
    subdrill = Column(DECIMAL(10, 0), nullable=True)

    drilling = relationship('Drilling_model')
    firing_type = relationship('firing_type')
    location = relationship('Location_openpit_model')


class Stockpile_balance_model(db.Model):
    __tablename__ = 'stockpile_balance'

    id = Column(Integer, primary_key=True)
    tonnes = Column(DECIMAL(10, 0), nullable=False)
    adjtonnes = Column(DECIMAL(10, 0), nullable=False)
    ounces = Column(DECIMAL(10, 0), nullable=False)
    adjounces = Column(DECIMAL(10, 0), nullable=False)
    grade = Column(DECIMAL(10, 0), nullable=False)
    adjgrade = Column(DECIMAL(10, 0), nullable=False)
    loadhaul_id = Column(ForeignKey('loadhaul_model.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location_id = Column(ForeignKey('location_openpit_model.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    loadhaul = relationship('Loadhaul_model')
    location = relationship('Location_openpit_model')


class Consumables_firing_model(db.Model):
    __tablename__ = 'consumables_firing'

    id = Column(Integer, primary_key=True)
    quantity = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    consumable_id = Column(ForeignKey('consumable.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    consumable = relationship('Consumable_model')
    firing = relationship('Firing_model')



class Firing_measure_model(db.Model):
    __tablename__ = 'firing_measure'

    id = Column(Integer, primary_key=True)
    quantity = Column(String(45), nullable=False)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                              onupdate=func.current_timestamp())
    measure_id = Column(ForeignKey('measure.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    firing_id = Column(ForeignKey('firing.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    firing = relationship('Firing_model')
    measure = relationship('Measure_model')




# t_plant_hour_has_loadhaul = Table(
#     'plant_hour_has_loadhaul', metadata,
#     Column('plant_hour_id', ForeignKey('plant_hour.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
#     Column('loadhaul_id', ForeignKey('loadhaul.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
# )
