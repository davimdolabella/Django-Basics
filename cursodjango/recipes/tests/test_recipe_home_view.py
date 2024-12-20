from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):

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
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe title', content)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(
            '<h1 class="center all"> No Recipes found here 😥</h1>',
            response.content.decode('utf-8')
        )
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_is_paginated(self):
        for i in range(4):
            kwargs = {'author_data':{ 'username':f'u{i}'}, 'slug':f're{i}'}
            self.make_recipe(**kwargs)
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 2)
        self.assertEqual(len(paginator.get_page(2)), 2)