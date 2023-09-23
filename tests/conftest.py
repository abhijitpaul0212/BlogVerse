import pytest
from project.app import create_app
from project.models.blog import Category
import json


# @pytest.fixture
# def app():
#     yield create_app()


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture
def globals():
    global_all_category_num = []
    global_all_category_name = []
    for cat in Category.objects.all():
        dict_cat = json.loads(cat.to_json())
        global_all_category_num.append(dict_cat['_id']['$oid'])
        global_all_category_name.append(dict_cat['category_name'])
    return global_all_category_name, global_all_category_num
