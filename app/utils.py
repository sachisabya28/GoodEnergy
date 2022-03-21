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
