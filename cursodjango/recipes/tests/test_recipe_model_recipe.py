from recipes.tests.test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from recipes import views
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='newCategory'),
            author=self.make_author(username='newUser'),
            title ='Recipe title',
            description ='Recipe description',
            slug ='new_recipe-slug',
            preparation_time =10,
            preparation_time_unit ='Minutos',
            servings =5,
            servings_unit ='Porções',
            preparation_steps ='Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title',65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit',65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
         setattr(self.recipe, field, 'a' * (max_length + 1) )
         with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')