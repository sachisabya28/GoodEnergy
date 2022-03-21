from logging import exception

try:
    from app import app
except exception as ex:
    print(ex)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
