from recipe_book import views


routes = [
    ('/', views.IndexView.as_view('index')),

    ('/login', views.LoginView.as_view('login')),
    ('/signup', views.SignupView.as_view('signup')),
    ('/logout', views.LogoutView.as_view('logout')),

    ('/recipes', views.GetRecipeListView.as_view('recipes')),
    ('/recipes/<slug>', views.GetRecipeView.as_view('get_recipe')),
    ('/recipe/add', views.CreateRecipeView.as_view('create_recipe')),
]
