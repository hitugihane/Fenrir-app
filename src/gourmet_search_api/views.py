import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings

HOTPEPPER_API_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = settings.HOTPEPPER_API_KEY

def index(request):#index.htmlを返す
    return render(request, 'index.html')

def shop_details(request):#shop_details.htmlを返す
    shop_id = request.GET.get('shopId')
    return render(request, 'shop_details.html', {'shopId': shop_id})

def fetch_shops(request):#店舗情報を取得する
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    radius = request.GET.get('radius', '1')
    page_number = request.GET.get('page', 1)

    if radius == '6':
        shops = fetch_and_combine_shops_with_multiple_points(latitude, longitude)
    else:
        shops = fetch_and_combine_shops(latitude, longitude, radius)

    paginator = Paginator(shops, 6)
    page_obj = paginator.get_page(page_number)

    data = {
        'shops': list(page_obj.object_list),
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number
    }

    return JsonResponse(data)

def calculate_surrounding_points(latitude, longitude, distance=0.02):#周辺の店舗情報を取得する
    points = [
        (latitude + distance, longitude),
        (latitude - distance, longitude),
        (latitude, longitude + distance),
        (latitude, longitude - distance),
    ]
    return points

def fetch_and_combine_shops_with_multiple_points(lat, lng):#周辺の店舗情報を取得する
    points = calculate_surrounding_points(lat, lng)
    responses = []
    for point in points:
        params = {
            'key': API_KEY,
            'lat': point[0],
            'lng': point[1],
            'range': 5,
            'format': 'json',
        }
        response = requests.get(HOTPEPPER_API_URL, params=params)
        if response.status_code == 200:
            responses += response.json()['results']['shop']

    all_shops = list({shop['id']: shop for shop in responses}.values())
    return all_shops

def fetch_and_combine_shops(lat, lng, range_value):#周辺の店舗情報を取得する
    params = {
        'key': API_KEY,
        'lat': lat,
        'lng': lng,
        'range': range_value,
        'format': 'json',
    }
    response = requests.get(HOTPEPPER_API_URL, params=params)
    shops = []
    if response.status_code == 200:
        shops = response.json()['results']['shop']
    
    return shops

def fetch_shop_details(request):#店舗情報を取得する
    shop_id = request.GET.get('shopId')
    params = {
        'key': API_KEY,
        'id': shop_id,
        'format': 'json',
    }
    response = requests.get(HOTPEPPER_API_URL, params=params)
    if response.status_code == 200:
        return JsonResponse(response.json()['results']['shop'][0])
    else:
        return JsonResponse({'error': 'Shop not found'}, status=404)
