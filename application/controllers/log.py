from flask import Flask, request, redirect, url_for, flash, abort
from flask import render_template
from flask import current_app as app
from flask_security import login_required
import flask_login
from application.models import *
from datetime import datetime

# ===============================================ADD TRACKER LOG ==========================================================

@app.route('/tracker/<int:id>/log/add', methods = ['GET', 'POST'])
@login_required
def add_tracker_log(id):
    # TODO Form validation
    tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=id).one_or_none()
    if tracker_data:
        datatypes = list(set([i.datatype for i in tracker_data.ttype]))
        data = {
            'id': tracker_data.id,
            'name': tracker_data.name,
            'description': tracker_data.description,
            'user_id': tracker_data.user_id,
            'settings': ",".join([i.value for i in tracker_data.settings]),
            'type': datatypes[0] if len(datatypes) > 0 else '',
            'choices': {i.id: (i.value if i.value else '') for i in tracker_data.ttype}
        }

        if request.method == 'GET':
            return render_template('tracker/log.html', tracker=data)
        else:
            if request.form['tid'] == str(id):
                try:
                    log = Tracker_log(tracker_id = tracker_data.id, note = request.form['lnote'], timestamp = datetime.strptime(request.form['ldate'], '%m/%d/%Y, %I:%M:%S %p'))
                    db.session.add(log)
                    db.session.commit()
                except:
                    app.logger.exception(f'Error ocurred while adding tracker log')
                    # if any internal error occurs, rollback the database
                    db.session.rollback()
                    flash('Internal error occurred, wasn\'t able to add tracker log', 'error')
                    return redirect(url_for('home_page'))
                
                try:
                    if data['type'] == 'ms':
                        choices = request.form['lchoice']
                        for i in choices:
                            x = Tracker_log_value(log_id = log.id, value = i)
                            db.session.add(x)                    
                        db.session.commit()
                    
                    else:
                        x = Tracker_log_value(log_id = log.id, value = request.form['lvalue'])
                        db.session.add(x)
                        db.session.commit()
                except:
                    app.logger.exception(f'Error ocurred while adding tracker log value')
                    # if any internal error occurs, rollback the database
                    db.session.rollback()
                    flash('Internal error occurred, wasn\'t able to add tracker log value', 'error')
                    return redirect(url_for('add_tracker_log', id=id))

                flash('Succesfully Saved tracker log', 'success')
                # TODO change to show_log page
                return redirect(url_for('home_page'))
            else:
                abort(404)
    
    else:
        abort(404)

# =========================================================================================================================


# =================================================EDIT TRACKER LOG =======================================================

@app.route('/tracker/<int:tracker_id>/log/<int:log_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_tracker_log(tracker_id, log_id):
    tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=tracker_id).one_or_none()    
    if tracker_data:
        log_data = Tracker_log.query.filter_by(tracker_id=tracker_data.id, id=log_id).one_or_none()
        if log_data:
            datatypes = list(set([i.datatype for i in tracker_data.ttype]))
            tdata = {
                'id': tracker_data.id,
                'name': tracker_data.name,
                'description': tracker_data.description,
                'user_id': tracker_data.user_id,
                'settings': ",".join([i.value for i in tracker_data.settings]),
                'type': datatypes[0] if len(datatypes) > 0 else '',
                'choices': {i.id: (i.value if i.value else '') for i in tracker_data.ttype}
            }

            ldata = {
                'id': log_data.id,
                'timestamp': log_data.timestamp,
                'note': log_data.note,
                'value': [i.value for i in log_data.values] 
            }

            if request.method == 'GET':
                return render_template('tracker/log.html', edit_mode = True, tracker = tdata, log = ldata)
            
            else:
                if request.form['tid'] == str(tracker_data.id) and request.form['lid'] == str(log_data.id):
                    try:
                        log_data.timestamp = datetime.strptime(request.form['ldate'], '%m/%d/%Y, %I:%M:%S %p')
                        log_data.note = request.form['lnote']
                        
                        for i in log_data.values:
                            db.session.delete(i)

                        if tdata['type'] == 'ms':
                            choices = request.form['lchoice']
                            for i in choices:
                                x = Tracker_log_value(log_id = log_data.id, value = i)
                                db.session.add(x)
                        
                        else:
                            x = Tracker_log_value(log_id = log_data.id, value = request.form['lvalue'])
                            db.session.add(x)
                        
                        db.session.commit()
                    except:
                        app.logger.exception(f'Error ocurred while editing tracker log with id {log_id}')
                        # if any internal error occurs, rollback the database
                        db.session.rollback()
                        flash('Internal error occurred, wasn\'t able to update tracker log value', 'error')
                        # TODO redirect to show_tracker page
                        return redirect(url_for('home_page'))
                    
                    flash('Succesfully updated tracker log', 'success')
                    # TODO change to show_log page
                    return redirect(url_for('home_page'))
                else:
                    abort(404)
        else:
            abort(404)
    else:
        abort(404)

# =========================================================================================================================


# =================================================EDIT TRACKER LOG =======================================================
@app.route('/tracker/<int:tracker_id>/log/<int:log_id>/delete', methods = ['GET'])
@login_required
def delete_tracker_log(tracker_id, log_id):
    # check if a tracker with the provided id and made by current user exists or not.
    tracker_data = Tracker.query.filter_by(user_id=flask_login.current_user.id, id=tracker_id).one_or_none()
    # if it exists, proceed.
    if tracker_data:
        log_data = Tracker_log.query.filter_by(tracker_id=tracker_data.id, id=log_id).one_or_none()
        if log_data:
            try:            
                db.session.delete(log_data)
                db.session.commit()
            except:
                app.logger.exception(f'Error ocurred while deleting tracker log with id {log_id}')
                # if any internal error occurs, rollback the database
                db.session.rollback()
                flash('Internal error occurred, wasn\'t able to delete tracker log', 'error')
                return redirect(url_for('home_page'))
        
            flash('Succesfully deleted tracker log', 'success')
            # TODO Redirect to show_log page
            return redirect(url_for('home_page'))
        else:
            abort(404)
    else:
        abort(404)

# =========================================================================================================================