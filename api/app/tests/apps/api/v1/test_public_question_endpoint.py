import os

from tests.apps.signals.factories import CategoryFactory, ParentCategoryFactory, QuestionFactory
from tests.test import SignalsBaseApiTestCase

THIS_DIR = os.path.dirname(__file__)


class TestCategoryQuestionEndpoints(SignalsBaseApiTestCase):
    def setUp(self):
        self.retrieve_sub_category_question_schema = self.load_json_schema(
            os.path.join(
                THIS_DIR,
                'json_schema',
                'get_signals_v1_public_questions_categories_{slug}_sub_categories_{sub_slug}.json'
            )
        )

        self.question = QuestionFactory.create_batch(5)
        self.parent_category = ParentCategoryFactory.create()
        CategoryFactory.create_batch(5, parent=self.parent_category, questions=self.question)
        self.parent_category.refresh_from_db()
        super(TestCategoryQuestionEndpoints, self).setUp()

    def test_sub_category_question_detail(self):
        sub_category = self.parent_category.children.first()

        url = '/signals/v1/public/questions/categories/{slug}/sub_categories/{sub_slug}'.format(
            slug=sub_category.parent.slug,
            sub_slug=sub_category.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # JSONSchema validation
        self.assertJsonSchema(self.retrieve_sub_category_question_schema, data)

        self.assertEqual(data['count'], 25)
