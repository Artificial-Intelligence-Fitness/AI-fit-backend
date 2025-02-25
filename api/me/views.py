from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        user = request.user  # Get the authenticated user
        return Response({
            "username": user.username,
            "email": user.email
        })
