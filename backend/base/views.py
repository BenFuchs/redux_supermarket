from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from .models import Cart, Product
from .serializers import ProfileSerializer, ProductSerializer

@api_view(['GET'])
def index(request):
    return Response('hello')

# register
@api_view(['POST'])
def register(request):
    try:
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        user.is_active = True
        user.is_staff = False
        user.save()
        return Response("New user created", status=status.HTTP_201_CREATED)
    except KeyError as e:
        return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# create profile
@api_view(['POST'])
def registerProfile(request):
    try:
        username = request.data.get('username')
        user = User.objects.get(username=username)
        profile_data = {
            'user': user.id,
            'phone_number': request.data.get('phoneNumber'),
            'address': request.data.get('address'),
            'age': request.data.get('age'),
            'gender': request.data.get('gender')
        }
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response("New Profile created", status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['isAdmin'] = user.is_superuser
        token['id'] = user.id
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#cart
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLoggedUserCart(request):
    # Extract the JWT token from the Authorization header
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        token = auth_header.split(' ')[1]
        
        try:
            # Decode the token using the secret key
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            # Log username and id
            username = decoded_token.get('username')
            user_id = decoded_token.get('id')
            
            print(f"Username: {username}, ID: {user_id}")
            
            # Query the Cart model to find active items for this user
            cart_items = Cart.objects.filter(userID=user_id)
            
            if cart_items.exists():
                # Prepare the cart data to return
                cart_data = [
                    {
                        "product_id": item.productID.id,
                        "amount": item.amount,
                        "date": item.date
                    }
                    for item in cart_items
                ]
                
                return Response({"message": "Cart items found", "cart": cart_data})
            else:
                return Response({"message": "No items in the cart for this user"})
        
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=401)
    
    return Response({"error": "Authorization header not provided"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addProductToUserCart(request):
    # Extract the JWT token from the Authorization header
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        token = auth_header.split(' ')[1]
        
        try:
            # Decode the token using the secret key
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            # Get the user id from the token
            user_id = decoded_token.get('id')
            
            # Ensure productID and amount are provided in the request body
            product_id = request.data.get('productID')
            amount = request.data.get('amount', 1)  # Default amount to 1 if not provided
            
            if not product_id:
                return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Check if the product is already in the user's cart
            cart_item, created = Cart.objects.get_or_create(
                userID_id=user_id,  # Use user_id from the JWT token
                productID=product,
                defaults={'amount': amount}  # Provide the amount during creation
            )
            
            if not created:
                # If the item already exists, update the amount
                cart_item.amount += amount
                cart_item.save()
            
            return Response({
                "message": "Product added to cart successfully",
                "product_id": product_id,
                "amount": cart_item.amount
            }, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({"error": "Authorization header not provided"}, status=status.HTTP_400_BAD_REQUEST)
