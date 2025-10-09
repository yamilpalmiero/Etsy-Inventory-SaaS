from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decouple import config
import requests
import secrets
from datetime import datetime, timedelta
from .models import Store


@login_required
def etsy_auth_init(request):
    """Inicia el proceso OAuth con Etsy"""
    
    # Generar code_verifier para PKCE
    code_verifier = secrets.token_urlsafe(32)
    request.session['code_verifier'] = code_verifier
    
    # Parámetros para la autorización
    client_id = config('ETSY_CLIENT_ID')
    redirect_uri = config('ETSY_REDIRECT_URI')
    scope = 'listings_r listings_w transactions_r'
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state
    
    # URL de autorización de Etsy
    auth_url = (
        f"https://www.etsy.com/oauth/connect"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&state={state}"
        f"&code_challenge={code_verifier}"
        f"&code_challenge_method=S256"
    )
    
    return redirect(auth_url)


@login_required
def etsy_auth_callback(request):
    """Recibe el callback de Etsy y obtiene los tokens"""
    
    # Verificar que el state coincida (seguridad)
    state = request.GET.get('state')
    if state != request.session.get('oauth_state'):
        messages.error(request, 'Error de seguridad en la autenticación')
        return redirect('store_list')
    
    # Obtener el código de autorización
    code = request.GET.get('code')
    if not code:
        messages.error(request, 'No se recibió código de autorización')
        return redirect('store_list')
    
    # Intercambiar código por tokens
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': config('ETSY_CLIENT_ID'),
        'code': code,
        'redirect_uri': config('ETSY_REDIRECT_URI'),
        'code_verifier': request.session.get('code_verifier')
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        tokens = response.json()
        
        # Obtener información de la tienda
        shop_info = get_shop_info(tokens['access_token'])
        
        # Guardar o actualizar la tienda
        store, created = Store.objects.update_or_create(
            owner=request.user,
            etsy_shop_id=shop_info['shop_id'],
            defaults={
                'shop_name': shop_info['shop_name'],
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'token_expires_at': datetime.now() + timedelta(seconds=tokens['expires_in'])
            }
        )
        
        action = 'conectada' if created else 'actualizada'
        messages.success(request, f'¡Tienda "{shop_info["shop_name"]}" {action} exitosamente!')
        
        return redirect('store_list')
        
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error al conectar con Etsy: {str(e)}')
        return redirect('store_list')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')
        return redirect('store_list')


def get_shop_info(access_token):
    """Obtiene información básica de la tienda desde Etsy"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': config('ETSY_CLIENT_ID')
    }
    
    # Primero obtenemos el user_id
    user_url = "https://openapi.etsy.com/v3/application/users/me"
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_id = user_response.json()['user_id']
    
    # Luego obtenemos las tiendas del usuario
    shops_url = f"https://openapi.etsy.com/v3/application/users/{user_id}/shops"
    shops_response = requests.get(shops_url, headers=headers)
    shops_response.raise_for_status()
    
    shops = shops_response.json()['results']
    if not shops:
        raise Exception("No se encontraron tiendas")
    
    # Retornar la primera tienda
    shop = shops[0]
    return {
        'shop_id': str(shop['shop_id']),
        'shop_name': shop['shop_name']
    }


@login_required
def store_list(request):
    """Lista las tiendas conectadas del usuario"""
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'stores/store_list.html', {'stores': stores})


@login_required
def store_disconnect(request, store_id):
    """Desconecta una tienda"""
    try:
        store = Store.objects.get(id=store_id, owner=request.user)
        shop_name = store.shop_name
        store.delete()
        messages.success(request, f'Tienda "{shop_name}" desconectada')
    except Store.DoesNotExist:
        messages.error(request, 'Tienda no encontrada')
    
    return redirect('store_list')