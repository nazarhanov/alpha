from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

  def setUp(self):
    self.client = Client()

  def testServiceStatus(self):
    res = self.client.post(reverse('status'))
    self.assertEquals(res.status_code, 200)

  def testIndexStatus(self):
    res = self.client.get(reverse('index'))
    self.assertEquals(res.status_code, 200)
