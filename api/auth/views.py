from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Creates user

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "refresh": str(refresh),
                "access": str(access)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
