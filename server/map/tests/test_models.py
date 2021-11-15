from django.test import TestCase
from map.models import *
from django.conf import settings
from sqlalchemy import *
from sqlalchemy.orm import *
import unittest
engine = settings.ENGINE

class CompanyModelTests(unittest.TestCase):
    # 作成削除Model内関数の挙動
    def setUp(self):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = Company()
        company.name = '鉄道会社井上'
        company.address = '東京都世田谷区松原1-43-14'
        company.founded = '1990年9月8日'
        company.created_at = '2021-06-12 04:36:28'
        company.updated_at = '2021-06-12 04:36:28'
        session.add(company)
        session.commit()
        session.close()

    def test_update(self):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.name=='鉄道会社井上').first()
        company.address = '東京都世田谷区松原'
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.name=='鉄道会社井上').first()
        self.assertEqual(company.address, '東京都世田谷区松原')
        session.close()

    def test_to_company_dict(self):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.id==1).first()
        values = list(company.to_company_dict().keys())
        self.assertEqual(len(values), 4)
        session.close()

    def test_to_company_dict(self):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.id==1).first()
        values = list(company.to_company_dict().keys())
        self.assertEqual(len(values), 4)
        session.close()

    def tearDown(self):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(Company).filter(Company.name=='鉄道会社井上').delete()
        session.commit()
        session.close()
    # def test_is_empty(self):
    #     """初期状態では何も登録されていないことをチェック"""
    #     saved_posts = Post.objects.all()
    #     self.assertEqual(saved_posts.count(), 0)

    # def test_is_count_one(self):
    #     """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
    #     post = Post(title='test_title', text='test_text')
    #     post.save()
    #     saved_posts = Post.objects.all()
    #     self.assertEqual(saved_posts.count(), 1)

    # def test_saving_and_retrieving_post(self):
    #     """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
    #     post = Post()
    #     title = 'test_title_to_retrieve'
    #     text = 'test_text_to_retrieve'
    #     post.title = title
    #     post.text = text
    #     post.save()

    #     saved_posts = Post.objects.all()
    #     actual_post = saved_posts[0]

    #     self.assertEqual(actual_post.title, title)
    #     self.assertEqual(actual_post.text, text)