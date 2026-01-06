from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('konta/login/', views.CustomLoginView.as_view(), name='login'),
    path('konta/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('konta/login/2fa/', views.CustomOTPLoginView.as_view(), name='otp_login'),
    path('rejestracja/', views.RejestracjaView.as_view(), name='rejestracja'),
    path('', views.IndexView.as_view(), name='index'),
    path('filmy/', views.FilmyView.as_view(), name='filmy'),
    path('film/<int:pk>/', views.FilmDetailView.as_view(), name='film-detail'),
    path('seanse/', views.SeanseView.as_view(), name='seanse'),
    path('seanse/<int:year>/<int:month>/<int:day>/', views.SeanseView.as_view(), name='seanse_data'),
    path('rezerwacja/<int:seans_id>/', views.RezerwacjaView.as_view(), name='rezerwacja'),
    path('konto/', views.KontoView.as_view(), name='konto'),
    path('konto/edytuj/', views.edytuj_profil, name='edytuj-profil'),
    path('konto/2fa/setup/', views.Setup2FAView.as_view(), name='2fa_setup'),
    path('admin-panel/', views.AdminView.as_view(), name='admin-panel'),
    path('o-nas/', views.InfoView.as_view(), name='info'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('kontakt/', views.KontaktView.as_view(), name='kontakt'),
    path('polityka-prywatnosci/', views.PolitykaPrywatnosciView.as_view(), name='polityka'),
    path('regulamin/', views.RegulaminView.as_view(), name='regulamin'),
    path('cookies/', views.CookiesView.as_view(), name='cookies'),
]