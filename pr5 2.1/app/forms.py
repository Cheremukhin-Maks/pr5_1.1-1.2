"""Views додатка app."""

from django.http import HttpResponse


def index(request):
    """Головна сторінка."""
    html_content = """
    <h1>Ласкаво просимо на наш сайт!</h1>
    <p>Це головна сторінка Django-додатка.</p>
    <ul>
        <li>Перший пункт списку</li>
        <li>Другий пункт списку</li>
        <li>Третій пункт списку</li>
    </ul>
    """
    return HttpResponse(html_content)


def about(request):
    """Сторінка 'Про проект'."""
    html_content = """
    <h1>Про проект</h1>
    <p><b>Курс:</b> Веб-розробка / Python Django</p>
    <p><b>Практична робота:</b> №5</p>
    <p><b>Студент:</b> [Ваше Ім'я]</p>
    """
    return HttpResponse(html_content)


def contact(request):
    """Контактна сторінка з параметрами запиту."""
    name = request.GET.get('name')
    if name:
        html_content = f"<h1>Привіт, {name}!</h1><p>Дякуємо, що зв'язалися з нами.</p>"
    else:
        html_content = "<h1>Контактна сторінка</h1><p>Вкажіть ім'я в URL (наприклад: /contact/?name=Іван).</p>"
    
    return HttpResponse(html_content)