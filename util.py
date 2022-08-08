from datetime import datetime


def success(data=None):
    if data is None:
        return {'message': 'success'}, 200

    return {
        'message': 'success',
        'data': data,
        'datatime': datetime.utcnow().isoformat()
    }, 200

def failure():
    return {"message": "failure"}, 500

def total(data=None,total=0):
    return {
               'message': 'success',
               'data': data,
               'datatime': datetime.utcnow().isoformat(),
               'totalPrice': f"$ {total}"
           }, 200