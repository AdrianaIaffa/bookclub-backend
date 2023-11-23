import logging
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, GroupSerializer, BookClubSerializer, UserRegistrationSerializer, CommentSerializer
from .models import BookClub, Comment


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookClubViewSet(viewsets.ModelViewSet):
    queryset = BookClub.objects.all()
    serializer_class = BookClubSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def detail(self, request):
        bookclub = self.get_object()
        serializer = self.get_serializer(bookclub)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        bookclub = self.get_object()
        comments = Comment.objects.filter(bookclub=bookclub)
        comment_serializer = CommentSerializer(comments, many=True)
        return Response(comment_serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the current user
        user = self.request.user

        # Create the book club with the user as the creator and first member
        serializer.save(created_by=user, members=[user])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['PUT'])
    def update_bookclub(self, request, pk=None):
        try:
            bookclub = self.get_object()
            serializer = self.get_serializer(bookclub, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"message": "Book club not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def join(self, request, pk=None):
        bookclub = self.get_object()
        user = request.user  

        if user not in bookclub.members.all():
            bookclub.members.add(user)
            return Response({"message": f"User {user.username} joined the book club successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"User {user.username} is already a member of the book club."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def leave(self, request, pk=None):
        bookclub = self.get_object()
        user = request.user  

        if user in bookclub.members.all():
            bookclub.members.remove(user)
            return Response({"message": f"User {user.username} left the book club successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"User {user.username} is not a member of the book club."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_bookclub(self, request, pk=None):
        bookclub = self.get_object()

        # Check if the current user is the creator of the book club
        if request.user == bookclub.created_by:
            bookclub.delete()
            return Response({"message": f"Book club '{bookclub.name}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You do not have permission to delete this book club."}, status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        bookclub = self.get_object()
        user = request.user

        # Check if the user is a member of the book club
        if user not in bookclub.members.all():
            return Response({"message": "You must join the book club to leave a comment."},
                            status=status.HTTP_403_FORBIDDEN)

        data = {
            'bookclub': bookclub.id,
            'user': user.id,
            'comment': request.data.get('comment'),
        }

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.body["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # permission_classes = [AllowAny]
