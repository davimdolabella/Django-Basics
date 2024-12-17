from recipes.tests.test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views

class RecipeDetailViewTest(RecipeTestBase):

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


    def test_recipe_detail_template_loads_the_correct_recipe(self):
        title = 'This is a detail test'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn(title, content)


    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe= self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', args=(recipe.id,)))
        self.assertEqual(response.status_code, 404)
    
