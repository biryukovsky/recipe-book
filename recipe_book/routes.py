from recipe_book import views


routes = [
    ('/', views.IndexView.as_view('index')),
    ('/login', views.LoginView.as_view('login')),
    ('/signup', views.SignupView.as_view('signup')),
    ('/logout', views.LogoutView.as_view('logout')),
]
