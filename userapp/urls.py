from .views import ProfileUpdateView, HealthcheckViewset, ProfileDeactivateView, ProfileActivateView
from .views import RegisterAdminView, GetAllUsersView, AssignRightsView, RegisterSuperAdminView
from .views import CrawlViewset, RegisterView, LoginView, LogoutView, PasswordResetView
from django.urls import path


urlpatterns = [
    path('healthmocker/', HealthcheckViewset.as_view({"get": "checker"}), name="healthmocker"),

    path('superadminregister/', RegisterSuperAdminView.as_view(), name="superadminregisters"),
    path('superadminlogin/', LoginView.as_view(), name="superadminlogins"),
    path('adminregister/', RegisterAdminView.as_view(), name="adminregisters"),
    path('adminlogin/', LoginView.as_view(), name="adminlogins"),
    path('register/', RegisterView.as_view(), name="registers"),
    path('login/', LoginView.as_view(), name="logins"),

    path('logout/', LogoutView.as_view(), name="logouts"),
    path('passwordreset/', PasswordResetView.as_view(), name="reset"),
    path('profileupdate/', ProfileUpdateView.as_view(), name="update"),
    path('accountdeactivate/', ProfileDeactivateView.as_view(), name="deactivate"),
    path('accountactivate/', ProfileActivateView.as_view(), name="activate"),

    path('allusers/', GetAllUsersView.as_view(), name="userlist"),
    path('usersrights/', AssignRightsView.as_view(), name="manage_user_rights"),

    path('crawling/', CrawlViewset.as_view({'post': 'crawlrequest'}), name="CrawlRequest"),
    path('search/', CrawlViewset.as_view({'post': 'searchrequest'}), name="SearchRequest"),


]
