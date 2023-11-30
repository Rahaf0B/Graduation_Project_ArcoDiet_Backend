import io
from django.shortcuts import render
from .serializers import AddProductSerializer, FavoriteProductSerializer
from .models import Product, FavoriteProducts
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from reqUser.models import User
from reqUser.jwt import JWTAuthentication
from django.core.mail import EmailMessage
from rest_framework.views import APIView


class AddProductAPIView(GenericAPIView):

    serializer_class = AddProductSerializer

    def post(self, request):
        count_product_added = 0
        count_product_already_added = 0

        for product in request.data['products']:
            try:
                product_added = Product.objects.get(
                    barcode_number=product["barcode_number"])
                count_product_already_added = count_product_already_added+1
            except:
                serializer = self.serializer_class(data=product)
                if serializer.is_valid():
                    serializer.save()
                    count_product_added = count_product_added+1

        if count_product_already_added > 0:
            return response.Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        elif count_product_added > 0:
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class getProductAPIView(GenericAPIView):

    serializer_class = AddProductSerializer

    def post(self, request):

        try:
            product_added = Product.objects.filter(
                barcode_number=request.data["barcode_number"]).values('product_id')
            serializer = AddProductSerializer(
                data=product_added.values().first())
            if serializer.is_valid():
                return response.Response(product_added.values().first(), status=status.HTTP_201_CREATED)

        except:
            return response.Response("this product is not available", status=status.HTTP_400_BAD_REQUEST)

        return response.Response("this product is not available", status=status.HTTP_400_BAD_REQUEST)


class getProductByIDAPIView(GenericAPIView):

    serializer_class = AddProductSerializer

    def get(self, request, product_id):

        try:
            product_added = Product.objects.filter(
                product_id=product_id).values('product_id')
            serializer = AddProductSerializer(
                data=product_added.values().first())

            if serializer.is_valid():
                return response.Response(product_added.values().first(), status=status.HTTP_201_CREATED)

        except:
            return response.Response("this product is not available", status=status.HTTP_400_BAD_REQUEST)

        return response.Response("this product is not available", status=status.HTTP_400_BAD_REQUEST)


class getALLProductsAPIView(GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = AddProductSerializer

    def get(self, request):
        queryset = Product.objects.all()
        serializer = AddProductSerializer(queryset, many=True)
        return response.Response(serializer.data)


class AddFavoriteProductsAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request, id):
        product = Product.objects.get(product_id=id)
        user = request.user

        try:
            FavoriteProductsInstance = FavoriteProducts.objects.get(user=user)
        except:
            FavoriteProductsInstance = FavoriteProducts.objects.create(
                user=user)

        FavoriteProductsInstance.product.add(product)
        FavoriteProductsInstance.save()
        return response.Response({'success': 'Favorite Products added.'}, status=status.HTTP_201_CREATED)


class DeleteFavoriteProductAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def put(self, request, id):
        product = Product.objects.get(product_id=id)
        user = request.user
        try:
            FavoriteProductsInstance = FavoriteProducts.objects.get(
                user=user, product=product)
            FavoriteProductsInstance.product.remove(product)
            FavoriteProductsInstance.save()
        except:
            ...

        return response.Response({'success': 'Favorite Product deleted.'}, status=status.HTTP_201_CREATED)


class GetAllFavoriteProductAPIView(GenericAPIView):
    permission_classes = ((permissions.IsAuthenticated,))
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        try:
            FavoriteProductsInstance = FavoriteProducts.objects.get(user=user)
            serializer = FavoriteProductSerializer(FavoriteProductsInstance)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return response.Response({'error': 'There is no Favorite Product'}, status=status.HTTP_404_NOT_FOUND)


class PictureEmailAPIView(APIView):
    def post(self, request, format=None):
        image = request.data['image']
        from_email = request.data['email']
        message = request.data['message']
        image_data = io.BytesIO(image.read())
        email = EmailMessage(
            subject='Add/Edit Product',
            body=message+"\n"+"From Email: " + from_email,
            from_email=from_email,
            to=['arcodiet@gmail.com'],
        )
        email.attach('image.png', image_data.read(), 'image/png')

        try:
            email.send()
            return response.Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HelpEmailAPIView(APIView):
    def post(self, request, format=None):

        from_email = request.data['email']
        message = request.data['message']

        email = EmailMessage(
            subject='Help and Support',
            body=message+"\n"+"From Email: " + from_email,
            from_email=from_email,
            to=['arcodiet@gmail.com'],
        )

        try:
            email.send()
            return response.Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
