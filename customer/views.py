from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from mssql_service import ERPDB


@api_view(['GET'])
def preview_order(request: Request) -> Response:
    is_am = request.query_params.get('isAm', '')
    is_am = True if is_am == 'true' else False
    erp_db = ERPDB()
    result: list = erp_db.get_order_data(is_am=is_am)
    return Response(data=result, status=200)
