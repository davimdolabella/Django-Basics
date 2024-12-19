import pytest
from django.test import TestCase
from django.urls import reverse
from utils.pagination import make_pagination_range, make_pagination
from recipes.models import Category, Recipe, User


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2,3,4,5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9,10,11,12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11,12,13,14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

    def test_current_page_is_1_if_ValueError(self):
        category = Category.objects.create(name='Café da Manhã')
        user = User.objects.create_user(
            first_name='Lara',
            last_name='Crosfit',
            email='laracrosfit@gmail.com',
            username='laracrosfit123',
            password='lara123'
        )
        for i in range (1, 101):
            Recipe.objects.create(
                category=category,
                author=user,
                title =f'Uma Recita({i})',
                description ='Recipe description',
                slug =f'recipe-slug({i})',
                preparation_time =10,
                preparation_time_unit ='Minutos',
                servings =5,
                servings_unit ='Porções',
                preparation_steps ='Preparation Steps',
                preparation_steps_is_html =False,
                is_published =True,
                cover='123',
        )
        recipes = Recipe.objects.all().order_by('-id')
        response = self.client.get(reverse('recipes:home') + '?page=abc')
        request = response.context['request']
        obj_pages, pagination_range = make_pagination(request, recipes, 9)
        self.assertEqual(pagination_range['current_page'], 1)
        
        

