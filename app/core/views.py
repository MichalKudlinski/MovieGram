from multiprocessing import AuthenticationError
from tokenize import Token
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from . import serializers
from .models import Director, Movie, Post, UserProfile, Comment

# Create your views here.


class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class DirectorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

@extend_schema_view(
    my_profile=extend_schema(
        parameters=[
            OpenApiParameter(
                'unfriend',
                OpenApiTypes.STR,
                description='Comma seperated list of friend_ids to unfriend'
            ),
            
        ]
    )
)
class UserProfileViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    # viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    # def get_serializer_class(self):
    #     if self.method == 'my_profie':
    #         return serializers.MyProfileSerializer
    #     return self.serializer_class

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    @ action(methods=["GET", "PATCH"], detail=False, permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        obj = UserProfile.objects.filter(user=self.request.user).get()
        unfriend= self.request.query_params.get('unfriend')
        if unfriend:
            unfriend_ids = self._params_to_ints(unfriend)
            friends=  obj.friends.filter(id__in=unfriend_ids)
            for friend in friends:
                obj.friends.remove(friend) # a tu nie 
                UserProfile.objects.filter(user=friend).get().friends.remove(self.request.user.id) #czemu tu musi byc id
                




        queryset = UserProfile.objects.filter(user=self.request.user).get()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class FriendsProfilesViewSet(viewsets.ModelViewSet): #tutaj zmiana na tylko get i retrieve tylko tak zeby dzialal router

    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        
        my_friends = [el.id for el in UserProfile.objects.filter(
            user=self.request.user).get().friends.all()]
        queryset = UserProfile.objects.filter(user__id__in=my_friends)
        return queryset

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'directors',
                OpenApiTypes.STR,
                description='Comma seperated list of directors that you are intersted in'
            ),
            
            
        ]
    )
)
class MainPageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostListingSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    


    def get_queryset(self):
        my_friends = [el.id for el in UserProfile.objects.filter(
            user=self.request.user).get().friends.all()]
        queryset = Post.objects.filter(user__id__in=my_friends)
        directors = self.request.query_params.get('directors')
        if directors:
            try:
                director_ids=[]
                for el in directors.split(','):
                    director_ids.append(Director.objects.get(name=el).id)
                queryset = queryset.filter(movie__director__in = director_ids)
            except:
                return queryset


        return queryset
    def create(self, request):
        serializer = serializers.PostCreatingSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(user=self.request.user)
        return Response (serializer.data)

    

class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


            




        
    