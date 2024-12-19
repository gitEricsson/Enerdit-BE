from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import GoogleSocialAuthSerializer
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from urllib.parse import urlencode
from typing import Dict, Any
from authentication.models import User
import requests

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f'{os.environ.get("APP_BASE_URL")}/login'

class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        
        validated_data = (serializer.validated_data)
                
        user_data = get_user_data(validated_data)
                
        if hasattr(user_data, 'status_code') and user_data.status_code != 200:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
                
        user = User.objects.get(email=user_data['email'])
        tokens = user.tokens()
                
        # Return a JSON response with tokens and redirect URL
        return Response({
            'status': 'success',
            'message': 'User authenticated successfully',
            'tokens': tokens,
            'user': {
                'user_id': user.id,
                **user_data
            }
        }, status=status.HTTP_200_OK)

# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
        'client_secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    
    if not response.ok:
        raise ValidationError('Could not get access token from Google.')
    
    access_token = response.json()['access_token']

    return access_token

# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )
    
    if not response.ok:
        raise ValidationError('Could not get user info from Google.')
    
    return response.json()


def get_user_data(validated_data):
    try :
        domain = os.environ.get("API_BASE_URL")
        redirect_uri = os.environ.get("GOOGLE_APP_REDIRECT_URI")
        code = validated_data.get('code')
        error = validated_data.get('error')
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{LOGIN_URL}?{params}')
                
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_get_user_info(access_token=access_token)
                
        # Creates user in DB if first time login
        User.objects.get_or_create(
            email = user_data['email'],
            name = f"{user_data.get('given_name')} {user_data.get('family_name')}" if user_data.get('family_name') else user_data.get('given_name'),
            auth_provider = 'google',
            is_verified = user_data['email_verified'],

        )
        
        profile_data = {
            'email': user_data['email'],
            'name': f"{user_data.get('given_name')} {user_data.get('family_name')}" if user_data.get('family_name') else user_data.get('given_name'),
        }
        return profile_data
    
    except IntegrityError:
        profile_data = {
            'email': user_data['email'],
            'name': f"{user_data.get('given_name')} {user_data.get('family_name')}" if user_data.get('family_name') else user_data.get('given_name'),
        }
        return profile_data
    
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)