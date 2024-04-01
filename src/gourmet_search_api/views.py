import requests
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import FavoriteShop
from django.views.decorators.http import require_POST

HOTPEPPER_API_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = settings.HOTPEPPER_API_KEY

def index(request):
    # トップページを表示します。
    return render(request, 'index.html')

def shop_details(request):
    # 特定の店舗の詳細情報を表示します。
    shop_id = request.GET.get('shopId')
    params = {
        'key': API_KEY,
        'id': shop_id,
        'format': 'json',
    }
    response = requests.get(HOTPEPPER_API_URL, params=params)
    if response.status_code == 200:
        shop_details = response.json()['results']['shop'][0]  # 店舗の詳細情報を取得
        return render(request, 'shop_details.html', {'shop': shop_details})
    else:
        return render(request, 'shop_details.html', {'error': 'Shop not found'})

def fetch_shops(request):
    # 周辺の店舗情報を取得します。
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

def calculate_surrounding_points(latitude, longitude, distance=0.02):
    # 周辺の点を計算します。
    points = [
        (latitude + distance, longitude),
        (latitude - distance, longitude),
        (latitude, longitude + distance),
        (latitude, longitude - distance),
    ]
    return points

def fetch_and_combine_shops_with_multiple_points(lat, lng):
    # 複数の点から店舗情報を取得し結合します。
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

def fetch_and_combine_shops(lat, lng, range_value):
    # 店舗情報を取得します。
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

def fetch_shop_details(request):
    # 単一の店舗情報を取得します。
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

@login_required
@require_POST
def add_to_favorites(request):
    try:
        # リクエストからJSONデータを読み込む
        data = json.loads(request.body)
        shop_id = data.get('shopId')
        
        if not shop_id:
            return JsonResponse({'status': 'error', 'message': 'Shop ID cannot be null'}, status=400)
        
        # FavoriteShopインスタンスの作成
        favorite_shop, created = FavoriteShop.objects.get_or_create(
            user=request.user,
            shop_id=shop_id
        )

        if created:
            # 新しくお気に入りに追加された場合
            return JsonResponse({'status': 'success', 'message': 'Shop successfully added to favorites.'})
        else:
            # 既にお気に入りに存在する場合
            return JsonResponse({'status': 'error', 'message': 'This shop is already in your favorites.'}, status=400)

    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def remove_from_favorites(request):
    # ユーザーのお気に入りから店舗を削除します。
    if request.method == "POST":
        shop_id = request.POST.get('shopId')
        FavoriteShop.objects.filter(user=request.user, shop_id=shop_id).delete()
        return JsonResponse({'status': 'success'})

def signup(request):
    # 新規ユーザー登録ページを表示します。
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def favorites(request):
    # 現在のユーザーのお気に入り店舗のIDのリストを取得
    favorite_shops_ids = FavoriteShop.objects.filter(user=request.user).values_list('shop_id', flat=True)
    favorite_shops = []

    # 各店舗IDに対してAPIから詳細情報を取得
    for shop_id in favorite_shops_ids:
        response = requests.get(f"{HOTPEPPER_API_URL}?key={API_KEY}&id={shop_id}&format=json")
        if response.status_code == 200:
            shop_details = response.json()['results']['shop'][0]
            favorite_shops.append(shop_details)

    # お気に入り店舗の情報をテンプレートに渡す
    return render(request, 'favorites.html', {'favorite_shops': favorite_shops})
