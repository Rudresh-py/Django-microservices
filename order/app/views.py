from .models import OderedProducts
from rest_framework.views import APIView
import requests
from rest_framework.response import Response

from .producer import publish


class OderProduct(APIView):
    def post(self, request, id):
        user_req = requests.get('http://localhost:8000/user')
        user_data = user_req.json()
        prod_req = requests.get(f'http://localhost:8000/products/{id}')
        prod_data = prod_req.json()

        try:
            user_id = user_data['id']
            prod_id = prod_data['id']
            prod_title = prod_data['title']

            ordered_product = OderedProducts(user_id=user_id,
                                             product_id=prod_id,
                                             product_tittle=prod_title)
            ordered_product.save()
            publish('product ordered', id)
        except:
            return Response({
                "error": 'errors '
            })

        return Response({
            'message': 'success'
        })
