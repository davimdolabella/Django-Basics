from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeTestBase(TestCase):

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
        
    def make_author(
        self, 
        first_name='Lara',
        last_name='Crosfit',
        email='laracrosfit@gmail.com',
        username='laracrosfit123',
        password='lara123'
        ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

    def make_recipe(
        self, 
        category_data=None,
        author_data=None,
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
        ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title =title,
            description =description,
            slug =slug,
            preparation_time =preparation_time,
            preparation_time_unit =preparation_time_unit,
            servings =servings,
            servings_unit =servings_unit,
            preparation_steps =preparation_steps,
            preparation_steps_is_html =preparation_steps_is_html,
            is_published =is_published,
            cover=cover,
        )