from .producer import publish

import requests

from .serializers import ProductSerializer, ProductUserSerializer
from .models import Product, ProductUser
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class LikeProduct(APIView):
    def post(self, request, id):
        req = requests.get('http://localhost:8000/user')
        data = req.json()
        try:
            user_id = data['id']
            product = Product.objects.get(id=id)
            product_user = ProductUser(user_id=user_id, product_id=product)
            product_user.save()
            publish('product_liked', id)
        except:
            return Response({
                "error": 'errors '
            })

        return Response({
            'message': 'success'
        })



