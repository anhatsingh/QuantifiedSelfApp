from flask import Flask, request, redirect, url_for, flash, abort
from flask import render_template
from flask import current_app as app
from flask_security import login_required
import flask_login
from application.models import *
from datetime import datetime, timedelta
import collections


# TODO Multi-Language support


# =============================================ADD TRACKER PAGE===========================================================
@app.route('/tracker/add', methods = ['GET', 'POST'])
@login_required
def add_tracker():
    # if the requested method is GET
    if request.method == 'GET':
        return render_template('tracker/add_edit.html', title='Add Tracker')
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

# =========================================================================================================================





# =============================================EDIT TRACKER PAGE===========================================================
@app.route('/tracker/<int:id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_tracker(id):
    # if the request method is get
    if request.method == 'GET':
        # check if a tracker with the provided id and made by current user exists or not.
        tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=id).one_or_none()
        # if it exists, proceed.
        if tracker_data:
            # collect all the data about the current tracker being edited.
            data = {
                'id': tracker_data.id,
                'name': tracker_data.name,
                'description': tracker_data.description,
                'user_id': tracker_data.user_id,
                'settings': ",".join([i.value for i in tracker_data.settings])
            }

            # get datatype of the tracker
            datatypes = list(set([i.datatype for i in tracker_data.ttype]))
            # set datatype to empty if no type is defined earlier
            data['type'] = datatypes[0] if len(datatypes) > 0 else ''
            # get all the choices of the tracker, replace NULL values with ''
            data['choices'] = "\n".join([i.value if i.value else '' for i in tracker_data.ttype]) if len(datatypes) > 0 else ''

            flash('Opened tracker', 'info')
            return render_template('tracker/add_edit.html', title=f'Edit Tracker {id}', edit_mode=True, tracker=data)
        
        else:
            # no such tracker found having id AND made by current_user
            abort(404)
    
    else:
        # TODO Add form validation
        # check if a tracker with the provided id and made by current user exists or not.
        tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=id).one_or_none()
        # if it exists, proceed. Additionally also check if tracker url id and form hidden field id matches or not.
        if tracker_data and id == int(request.form['tid']):
            try:
                # update values of tracker
                tracker_data.name = request.form['tname']
                tracker_data.description = request.form['tdescription']

                # delete all the old settings of a tracker
                for i in Settings.query.filter_by(tracker_id=id).all():
                    db.session.delete(i)
                
                # add new settings for the tracker
                for i in request.form['tsettings'].replace(' ', '').strip().split(','):
                    # make settings object
                    new_setting = Settings(tracker_id = tracker_data.id, value = i)
                    # add the details of new settings to db session
                    db.session.add(new_setting)
                
                # delete old data_types for the tracker
                for i in Tracker_type.query.filter_by(tracker_id=id).all():
                    db.session.delete(i)
                


                # add new data types for the tracker
                ttype = request.form['ttype']
                # if tracker type is multiple select
                if ttype == 'ms':
                    # get all the choices splitted across the \n
                    tchoices = request.form['tchoices'].strip().split('\n')
                    # add each choice to the database
                    for i in tchoices:
                        new_choice = Tracker_type(tracker_id  = tracker_data.id, datatype = ttype, value = i)
                        db.session.add(new_choice)
                
                # if tracker type is integer values
                elif ttype == 'integer':
                    new_choice = Tracker_type(tracker_id  = tracker_data.id, datatype = ttype, value = None)
                    db.session.add(new_choice)
                
                # if tracker type is float values
                elif ttype == 'float':
                    new_choice = Tracker_type(tracker_id  = tracker_data.id, datatype = ttype, value = None)
                    db.session.add(new_choice)
                
                # commit all the above changes to the database
                db.session.commit()
            
            except:
                app.logger.exception(f'Error ocurred while editing tracker with id {id}')
                # if any internal error occurs, rollback the database
                db.session.rollback()
                flash('Internal error occurred, wasn\'t able to update tracker', 'error')
                return redirect(url_for('edit_tracker', id=id))
            
            flash('Succesfully updated tracker info', 'success')
            return redirect(url_for('home_page'))
        else:
            abort(404)

# =========================================================================================================================




# ============================================DELETE TRACKER PAGE==========================================================
@app.route('/tracker/<int:id>/delete', methods = ['GET'])
@login_required
def delete_tracker(id):
    # check if a tracker with the provided id and made by current user exists or not.
    tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=id).one_or_none()
    # if it exists, proceed.
    if tracker_data:
        try:            
            db.session.delete(tracker_data)
            db.session.commit()
        except:
            app.logger.exception(f'Error ocurred while deleting tracker with id {id}')
            # if any internal error occurs, rollback the database
            db.session.rollback()
            flash('Internal error occurred, wasn\'t able to delete tracker', 'error')
            return redirect(url_for('home_page'))
        
        flash('Succesfully deleted tracker', 'success')
        return redirect(url_for('home_page'))
    else:
        abort(404)

# =========================================================================================================================

# =================================================SHOW TRACKER INFO=======================================================
@app.route('/tracker/<int:id>/show', methods = ['GET', 'POST'], defaults= {'period': 'w'})
@app.route('/tracker/<int:id>/show/<string:period>', methods = ['GET', 'POST'])
@login_required
def show_tracker_log(id, period):
    # check if a tracker with the provided id and made by current user exists or not.
    tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=id).one_or_none()
    # if it exists, proceed.
    if tracker_data:
        datatypes = list(set([i.datatype for i in tracker_data.ttype]))
        tdata = {
            'id': tracker_data.id,
            'name': tracker_data.name,
            'description': tracker_data.description,
            'user_id': tracker_data.user_id,
            'settings': ",".join([i.value for i in tracker_data.settings]),
            'type': datatypes[0] if len(datatypes) > 0 else '',
            'choices': {i.id: (i.value.strip() if i.value else '') for i in tracker_data.ttype}
        }
        log_data = []
        chart_data = {}
        for i in tracker_data.values:
            this_data = {
                'id': i.id,
                'timestamp': i.timestamp,
                'note': i.note,
                'value': [tdata['choices'][int(x.value)] for x in i.values] if tdata['type'] == 'ms' else [x.value for x in i.values]
            }
            log_data.append(this_data)

            if tdata['type'] == 'ms':                
                options = list(set(this_data['value']))
                for i in options:
                    if i in chart_data:
                        chart_data[i] += this_data['value'].count(i)
                    else:
                        chart_data[i] = this_data['value'].count(i)
            
            else:                
                difference_in_time = datetime.today() - this_data['timestamp']
                if period == 'w' and difference_in_time.days <= 7:
                    ts = datetime.strftime(i.timestamp, "%Y-%m-%d")
                    include = True
                elif period == 'm' and difference_in_time.days <= 30:
                    ts = datetime.strftime(i.timestamp, "%Y-%m-%d")                
                    include = True
                elif period == 'd' and difference_in_time.days <= 0:
                    ts = datetime.strftime(i.timestamp, "%H:00")                    
                    include = True
                elif period == 'a':
                    ts = datetime.strftime(i.timestamp, "%Y-%m-%d")
                    include = True
                
                if include:
                    if ts in chart_data:
                        chart_data[ts] += int("".join(this_data['value'])) if tdata['type'] == 'integer' else float("".join(this_data['value']))
                    else:
                        chart_data[ts] = int("".join(this_data['value'])) if tdata['type'] == 'integer' else float("".join(this_data['value']))

        if tdata['type'] != 'ms':
            if period == 'w':
                delta = 7
                for i in range(delta):
                    key = datetime.strftime(datetime.today()-timedelta(i), "%Y-%m-%d")
                    if key not in chart_data:
                        chart_data[key] = 0
            elif period == 'm':
                delta = 30
                for i in range(delta):
                    key = datetime.strftime(datetime.today()-timedelta(i), "%Y-%m-%d")
                    if key not in chart_data:
                        chart_data[key] = 0
            elif period == 'd':
                delta = 24
                for i in range(delta):
                    key = datetime.strftime(datetime.today()-timedelta(hours=i), "%H:00")
                    if key not in chart_data:
                        chart_data[key] = 0
        
        return render_template('tracker/show.html', tracker = tdata, logs = log_data, period = period, total=len(tracker_data.values), chart=collections.OrderedDict(sorted(chart_data.items())))


# =========================================================================================================================