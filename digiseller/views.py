from django.shortcuts import render
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def verify_code(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'digiseller/error.html', {'message': 'Код не предоставлен'})

    # Проверка кода через API Digiseller
    try:
        response = requests.get(
            f"{settings.DIGISELLER_API_URL}check_code",
            params={
                'code': code,
                'api_key': settings.DIGISELLER_API_KEY
            }
        )
        data = response.json()

        if data.get('status') == 'success':
            # Перенаправление на oplata.info с информацией о покупке
            return redirect(f"https://oplata.info/verify?code={code}&status=success")
        else:
            return render(request, 'digiseller/error.html', {'message': 'Неверный код'})

    except Exception as e:
        return render(request, 'digiseller/error.html', {'message': 'Ошибка при проверке кода'})
