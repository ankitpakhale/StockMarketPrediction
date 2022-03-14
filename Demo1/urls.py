
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from pred_app.views import redirect_root, search
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_root),
	path('pred_app/', include('pred_app.urls')),
    path('search/<str:se>/<str:stock_symbol>/', search, name='predict_stock'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)