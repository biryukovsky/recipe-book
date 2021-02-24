from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from slugify import slugify, UniqueSlugify

from recipe_book.models import User, Recipe, Ingredient
from recipe_book.decorators import anonymous_required


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')


# Auth

class LoginView(MethodView):
    decorators = [anonymous_required, ]

    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = current_app.db_session.query(User).filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('index'))


class SignupView(MethodView):
    decorators = [anonymous_required, ]

    def get(self):
        return render_template('signup.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = current_app.db_session.query(User).filter_by(username=username).first()
        if user:
            return redirect(url_for('signup'))

        new_user = User(username=username,
                        password=generate_password_hash(password))
        current_app.db_session.add(new_user)
        current_app.db_session.commit()

        login_user(new_user)

        return redirect(url_for('recipes'))


class LogoutView(MethodView):
    decorators = [login_required, ]

    def get(self):
        logout_user()
        return redirect(url_for('index'))


# Recipe

class GetRecipeListView(MethodView):
    def get(self):
        recipes = current_app.db_session.query(Recipe).order_by(Recipe.created_at.desc())
        ctx = {
            'recipes': recipes,
        }
        return render_template('recipe_list.html', **ctx)


class GetRecipeView(MethodView):
    def get(self, slug):
        recipe = (current_app.db_session
                  .query(Recipe)
                  .join(Recipe.ingredients)
                  .filter(Recipe.slug == slug)
                  .first())
        ctx = {
            'recipe': recipe,
        }
        return render_template('recipe.html', **ctx)


class CreateRecipeView(MethodView):
    decorators = [login_required, ]

    def get(self):
        return render_template('create_recipe.html')

    def post(self):
        title = request.form.get('title')
        cooking_time = request.form.get('cooking_time')
        ingredient_names = request.form.getlist('ingredient[]')
        amount = request.form.getlist('amount[]')
        instruction = request.form.get('instruction')

        slug = make_unique_slug(title)

        recipe = Recipe(title=title,
                        cooking_time=cooking_time,
                        instruction=instruction,
                        slug=slug,
                        user_id=current_user.id)

        for ing, am in zip(ingredient_names, amount):
            recipe.ingredients.append(Ingredient(name=ing,
                                                 amount=am,
                                                 recipe_id=recipe.id))

        current_app.db_session.add(recipe)
        current_app.db_session.commit()

        return redirect(url_for('get_recipe', slug=recipe.slug))


def check_slug_exists(text, uids):
    if text in uids:
        return False
    slug = slugify(text, to_lower=True, max_length=30)
    sess = current_app.db_session

    recipe_exists = (
        sess.query(
            sess
            .query(Recipe)
            .filter_by(slug=slug)
            .exists()
        )
    ).scalar()
    return not recipe_exists


def make_unique_slug(title):
    slugifier = UniqueSlugify(unique_check=check_slug_exists, to_lower=True, max_length=30)
    return slugifier(title)
