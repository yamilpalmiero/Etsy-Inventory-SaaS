from datetime import datetime, timedelta
import requests
from decouple import config


def refresh_etsy_token(store):
    """Refresca el access token de Etsy"""
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    
    data = {
        'grant_type': 'refresh_token',
        'client_id': config('ETSY_CLIENT_ID'),
        'refresh_token': store.refresh_token
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        tokens = response.json()
        
        store.access_token = tokens['access_token']
        store.refresh_token = tokens['refresh_token']
        store.token_expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])
        store.save()
        
        return store
    except requests.exceptions.RequestException as e:
        print(f"Error refrescando token: {e}")
        return None


def get_valid_token(store):
    """Obtiene un token válido, refrescando si es necesario"""
    # Si el token expira en menos de 5 minutos, refrescar
    if store.token_expires_at <= datetime.now() + timedelta(minutes=5):
        store = refresh_etsy_token(store)
        if not store:
            return None
    
    return store.access_token