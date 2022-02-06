from logging import exception

try:
    from app import app
except exception as ex:
    print(ex)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)