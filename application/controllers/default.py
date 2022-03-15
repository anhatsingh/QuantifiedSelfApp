from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask import current_app as app
from flask_security import login_required
import flask_login
from application.models import *


# ================================================HOME PAGE===============================================================
# default home page, required to login to see
@app.route('/')
@login_required
def home_page():
    # this will contain info about trackers of this logged in user
    trackers = []
    # get all trackers made by this user
    for i in Tracker.query.filter_by(user_id=flask_login.current_user.id).all():
        # get the last updated value of this tracker
        updated_at = Tracker_log.query.filter_by(tracker_id=i.id).order_by(Tracker_log.timestamp.desc()).one_or_none()
        updated_at = updated_at if updated_at else "Never"
        # add the info gathered to the list of trackers above.
        trackers.append({'id': i.id, 'name': i.name, 'updated_at': updated_at})
    return render_template('home.html', title='test', trackers = trackers)

# ========================================================================================================================

# =============================================ADD TRACKER PAGE===========================================================
@app.route('/tracker/add', methods = ['GET', 'POST'])
@login_required
def add_tracker():
    # if the requested method is GET
    if request.method == 'GET':
        # TODO change tracker_type
        return render_template('tracker/add.html', title='Add Tracker')
    else:
        # TODO validation of input data
        try:
            # get the new tracker's object
            new_tracker = Tracker(name = request.form['tname'], description = request.form['tdescription'], user_id=flask_login.current_user.id)
            # add the detais of new tracker to database session
            db.session.add(new_tracker)
            # commit the session
            db.session.commit()
        except:
            # some internal error occurred
            app.logger.exception('Error occurred while creating a new tracker.')
            # rollback whatever the last session changes were.
            db.session.rollback()            
            # set error flash message
            flash('There was an error adding the tracker, please try again', 'error')
            # redirect to add_tracker page
            return redirect(url_for('add_tracker'))
        
        try:
            # get all the settings, remove spaces and split by comma
            for i in request.form['tsettings'].replace(' ', '').strip().split(','):
                # make settings object
                new_setting = Settings(tracker_id = new_tracker.id, value = i)
                # add the details of new settings to db session
                db.session.add(new_setting)
            
            # commit all the changes commited to settings so far
            db.session.commit()
        except:
            # some internal error occurred
            app.logger.exception('Error occurred while adding settings to the new tracker.')
            # rollback whatever the last session changes were.
            db.session.rollback()            
            # set error flash message
            flash('There was an error adding the settings, please edit the tracker info to add settings', 'error')
            # redirect to home page
            return redirect(url_for('home_page'))
        
        try:
            # get all the settings, remove spaces and split by comma
            ttype = request.form['ttype']
            # if tracker type is multiple select
            if ttype == 'ms':
                # get all the choices splitted across the \n
                tchoices = request.form['tchoices'].strip().split('\n')
                # add each choice to the database
                for i in tchoices:
                    new_choice = Tracker_type(tracker_id  = new_tracker.id, datatype = ttype, value = i)
                    db.session.add(new_choice)
            
            # if tracker type is integer values
            elif ttype == 'integer':
                new_choice = Tracker_type(tracker_id  = new_tracker.id, datatype = ttype, value = None)
                db.session.add(new_choice)
            
            # if tracker type is float values
            elif ttype == 'float':
                new_choice = Tracker_type(tracker_id  = new_tracker.id, datatype = ttype, value = None)
                db.session.add(new_choice)

            # commit all the changes commited to settings so far
            db.session.commit()
        except:
            # some internal error occurred
            app.logger.exception('Error occurred while adding Tracker Type to the new tracker.')
            # rollback whatever the last session changes were.
            db.session.rollback()            
            # set error flash message
            flash('There was an error setting the tracker type, please edit the tracker info to change the type', 'error')
            # redirect to home page
            return redirect(url_for('home_page'))


        # set success flash message to be displayed on home page
        flash('Successfully added Tracker', 'success')
        # redirect to home page
        return redirect(url_for('home_page'))

# ========================================================================================================================