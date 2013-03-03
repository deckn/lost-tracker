from flask import Flask, render_template, abort, jsonify
from lost_tracker.models import (Group, Station, get_state,
        advance as db_advance, STATE_FINISHED, STATE_UNKNOWN, STATE_ARRIVED)
from lost_tracker.database import db_session as session
app = Flask(__name__)


@app.route('/')
def index():
    stations = Station.query
    stations = stations.order_by(Station.order)
    stations = stations.all()
    groups = Group.query
    groups = groups.order_by(Group.order)
    groups = groups.all()

    state_matrix = []
    for group in groups:
        tmp = [group]
        for station in stations:
            tmp.append(get_state(group.id, station.id))
        state_matrix.append(tmp)

    sums = []
    if state_matrix:
        sums = [[0, 0, 0] for _ in state_matrix[0][1:]]
        for row in state_matrix:
            for i, elem in enumerate(row[1:]):
                if not elem or elem[0][0] == STATE_UNKNOWN:
                    sums[i][STATE_UNKNOWN] += 1
                elif elem[0][0] == STATE_ARRIVED:
                    sums[i][STATE_ARRIVED] += 1
                elif elem[0][0] == STATE_FINISHED:
                    sums[i][STATE_FINISHED] += 1

    return render_template('matrix.html',
            matrix=state_matrix,
            stations=stations,
            sums=sums)


@app.route('/advance/<groupId>/<station_id>')
def advance(groupId, station_id):
    new_state = db_advance(groupId, station_id)
    return jsonify(
            group_id=groupId,
            station_id=station_id,
            new_state=new_state)


@app.route('/station/<path:name>')
def station(name):
    qry = session.query(Station)
    qry = qry.filter_by( name = name )
    station = qry.first()
    if not station:
        return abort(404)

    groups = Group.query
    groups = groups.order_by(Group.order)
    groups = groups.all()
    return render_template('station.html',
            station=station,
            group_states=[(grp, get_state(grp.id, station.id))
                          for grp in groups])

if __name__ == '__main__':
    app.run(debug=True)
