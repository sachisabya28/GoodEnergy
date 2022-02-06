import csv
import io
import json
from flask import request
from app import app
from app.models import Location
from app import db

# define Python user-defined exceptions
class ValidationException(Exception):
    """Raise custom user defined Exception"""
    pass


def build_response(statuscode, body=None):
    """[Custom response bulder]

    Args:
        statuscode ([int])
        body ([string], optional): Defaults to None.

    Returns:
        [Dict]: [JSON body in response]
    """
    response = {
        "statusCode": statuscode,
    }
    if body is not None:
        response['body'] = body
    return response


@app.route('/health', methods=['GET', ])
def get_health():
    """
    Returns:
        [Dict]: [JSON body Health status]
    """
    return build_response(200, 'HEALTHY')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    try:
        uploaded_file = request.files['file']
        if not uploaded_file.filename.endswith('.csv'):
            return build_response(400, 'THIS IS NOT A CSV FILE')
        if uploaded_file.filename != '':
            parseCSV(uploaded_file)
            return build_response(200, 'Data Processed succesfully')
    except Exception:
        return build_response(400, 'Data not processed')


def parseCSV(filePath, skipHeader=None):
    data_set = filePath.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    #header is not required to be inserted db
    if skipHeader is None:
        skipHeader = True
    csv_data = csv.reader(io_string, delimiter=',')
    for row in csv_data:
        if skipHeader:
            skipHeader = False
        location = Location(row[0], row[1], row[2], row[3],
                            row[4], row[5], row[6])
        db.session.add(location)
        db.session.commit()
    return


@app.route('/userdata', methods=['POST']) 
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
        request_data = json.loads(request.data)
        if 'postal_code' not in request_data or \
                'city' not in request_data or \
                'street' not in request_data or \
                'house_number' not in request_data or \
                'yearly_kwh_consumption' not in request_data:
            raise ValidationException
        
        data = Location.query.filter_by(postal_code=request_data['postal_code'],
                                        city=request_data['city'],
                                        street=request_data['street'],
                                        house_number=str(request_data['house_number'])).all()
        # return if no data is found for User
        if len(data) == 0:
            return build_response(400, "No data found")
        total_unit_price, total_grid_fees, total_kwh_price = 0, 0, 0
        for val in data:
            total_unit_price += val.unit_price
            total_grid_fees += val.grid_fees
            total_kwh_price += val.kwh_price
        if len(data) > 1:
            avg_unit_price = total_unit_price/len(data)
            avg_grid_fees = total_grid_fees/len(data)
            avg_kwh_price = total_kwh_price/len(data)
            total_price = avg_unit_price + avg_grid_fees + \
                (request_data['yearly_kwh_consumption'] * avg_kwh_price)
            response = {
                "unit_price": avg_unit_price,
                "grid_fees": avg_grid_fees,
                "kwh_price": avg_kwh_price,
                "total_price": total_price,
            }
        else:
            total_price = total_unit_price + total_grid_fees + \
                (request_data['yearly_kwh_consumption'] * total_kwh_price)
            response = {
                "unit_price": total_unit_price,
                "grid_fees": total_grid_fees,
                "kwh_price": total_kwh_price,
                "total_price": total_price,
            }
        return response
    except ValidationException:
        return build_response(400, 'Bad JSON format')
    except Exception as e:
        return build_response(e.status_code, str(e))
    