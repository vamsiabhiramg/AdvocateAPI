

from django.shortcuts import render , redirect
from rest_framework import viewsets
# Add other necessary imports here
import requests 
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
from django.db.models import Q

from rest_framework.views import APIView


from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer

from dotenv import load_dotenv
load_dotenv()
import os

# Create your views here.

# GET /advocates
# POST /advocates

# GET /advocates/ :id
# PUT /advocates/:id
# DELETE /advocates/:id

TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')

@api_view(['GET'])
def endpoints(request):
    print('TWITTER_API_KEY:', TWITTER_API_KEY)
    data=['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def advocate_list(request):
    #Handles GET requests
    if request.method == 'GET':
        query= request.GET.get('query')
    
        if query==None:
            query=''
        
    
    
        #data=['Dennis','Tadas','Max']
        advocates=Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer= AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)



    if request.method =='POST':
        advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
            )
        
        serializer=AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
        
import time
class AdvocateDetail(APIView):
    
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise NotFound('Advocate does not exist!')
    
    def get(self, request, username):
        
        
        head={'Authorization': f'Bearer {TWITTER_API_KEY}',}
        
        fields = '?user.fields=profile_image_url,description,public_metrics'
        
        url="https://api.x.com/2/users/by/username/" + str(username) + fields
        twitter_response=requests.get(url, headers=head)
        if twitter_response.status_code != 200:
            return Response(
                {'error': f'Twitter API request failed with status code {twitter_response.status_code}', 'details': twitter_response.text},
                status=twitter_response.status_code
            )

        twitter_data = twitter_response.json()
        
        if 'data' in twitter_response:
            data = twitter_response['data']
            print('DATA FROM TWITTER:', data)
        else:
            return Response({'error': 'Twitter user not found'}, status=404)
        
        data['profile_image_url']=data['profile_image_url'].replace('normal', "400x400")
        #data=response['data']
        
        #print('DATA FROM TWITTER:', data)
        advocate=self.get_object(username)
        advocate.name=data['name']
        advocate.profile_pic=data['profile_image_url']
        advocate.bio=data['description']
        advocate.twitter='https://x.com/' + username
        advocate.save()
        print('User Updated!')
        serializer=AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):
        advocate=self.get_object(username)
        
        advocate.username=request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer=AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def delete(self, request, username):
        advocate=self.get_object(username)
        advocate.delete()
        return Response('user was deleted')
        
        


# @api_view(['GET', 'PUT','DELETE'])
# def advocate_detail(request,username):
#     advocate=Advocate.objects.get(username=username)

    
#     if request.method =='GET':
#         serializer=AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         advocate.username=request.data['username']
#         advocate.bio = request.data['bio']
        
#         advocate.save()
        
#         serializer=AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method =='DELETE':
#         advocate.delete()
#         return Response('user was deleted')
        
        
@api_view(['GET'])
def companies_list(request):
    companies=Company.objects.all()
    serializer=CompanySerializer(companies, many=True)
    return Response(serializer.data)

