from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User

class RecipeViewsTest(TestCase):

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1 class="center all"> No Recipes found here 😥</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_views_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='Lara',
            last_name='Crosfit',
            email='laracrosfit@gmail.com',
            username='laracrosfit123',
            password='lara123'
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title ='Recipe title',
            description ='Recipe description',
            slug ='recipe-slug',
            preparation_time =10,
            preparation_time_unit ='Minutos',
            servings =5,
            servings_unit ='Porções',
            preparation_steps ='Preparation Steps',
            preparation_steps_is_html =False,
            is_published =True,
            cover='123',
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe title', content)


    def test_recipe_category_views_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
             reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)


    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
             reverse('recipes:recipe', kwargs={'id': 10000})
        )
        self.assertEqual(response.status_code, 404)