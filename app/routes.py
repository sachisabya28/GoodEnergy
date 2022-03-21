import csv
import io
import json
from flask import request, jsonify
from app import app
from app.models import Location
from app import db
from app import utils, exceptions

@app.route('/health', methods=['GET', ])
def get_health():
    """
    Returns:
        [Dict]: [JSON body Health status]
    """
    return utils.build_response(200, 'HEALTHY')


# Get the uploaded files
@app.route("/upload", methods=['POST'])
def uploadFiles():
    try:
        uploaded_file = request.files['file']
        if not uploaded_file.filename.endswith('.csv'):
            return utils.build_response(400, 'THIS IS NOT A CSV FILE')
        if uploaded_file.filename != '':
            parseCSV(uploaded_file, True)
            return utils.build_response(200, 'Data Processed succesfully')
    except Exception as ex:
        print(ex)
        return utils.build_response(400, ex)


def parseCSV(filePath, skipHeader=None):
    data_set = filePath.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    csv_data = csv.reader(io_string, delimiter=',')
    for row in csv_data:
        if skipHeader:
            skipHeader = False
        else:
            house_number_start = int(row[3].split('-')[0])
            house_number_end = int(row[3].split('-')[1])
            location = Location(row[0], row[1], row[2], house_number_start,
                                house_number_end, row[4], row[5], row[6])
            location.save()
    return jsonify('data processed')


@app.route('/userdata', methods=['GET']) 
def get_price_user():
    """[receives the user location data and prices]

    Raises:
        ValidationException

    Returns:
        [Dict]: 
        "unit_price": <value>,
        "grid_fees": <value>,
        "kwh_price": <value>,
        "total_price": <value>
    """
    try:
        postal_code = request.args.get('postal_code', None)
        if postal_code is None:
            return utils.build_response(400, 'postal_code is not passed')

        city = request.args.get('city', None)
        if city is None:
            return utils.build_response(400, 'City is not passed')

        street = request.args.get('street', None)
        if street is None:
            return utils.build_response(400, 'street is not passed')

        house_number = request.args.get('house_number', None)
        if house_number is None:
            return utils.build_response(400, 'house_number is not passed')

        yearly_kwh_consumption = request.args.get('yearly_kwh_consumption', None)
        if yearly_kwh_consumption is None:
            return utils.build_response(400, 'yearly_kwh_consumption is not passed')

        data = Location.query.filter(Location.postal_code == int(postal_code),
                                    Location.city == str(city),
                                    Location.street == str(street),
                                    Location.house_number_start <= int(house_number),
                                    Location.house_number_end >= int(house_number)).all()
        # return if no data is found for Location
        if len(data) == 0:
            return utils.build_response(400, "No data found")
        total_unit_price, total_grid_fees, total_kwh_price = 0, 0, 0
        for val in data:
            total_unit_price += val.unit_price
            total_grid_fees += val.grid_fees
            total_kwh_price += val.kwh_price
        avg_unit_price = total_unit_price/len(data)
        avg_grid_fees = total_grid_fees/len(data)
        avg_kwh_price = total_kwh_price/len(data)
        total_price = avg_unit_price + avg_grid_fees + \
            (int(yearly_kwh_consumption) * avg_kwh_price)
        response = {
            "unit_price": avg_unit_price,
            "grid_fees": avg_grid_fees,
            "kwh_price": avg_kwh_price,
            "total_price": total_price,
        }

        return response
    except Exception as e:
        print(e)
    