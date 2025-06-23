"""
测试数据生成器 - 生成各种类型的测试数据
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from faker import Faker

class DataGenerator:
    """测试数据生成器"""
    
    def __init__(self, locale='zh_CN'):
        self.fake = Faker(locale)
        self.fake.seed_instance(4321)  # 确保可重现的结果
        
    def generate_data(self, data_type: str, count: int = 10) -> str:
        """根据数据类型生成测试数据"""
        
        generators = {
            'user': self._generate_user_data,
            'product': self._generate_product_data,
            'order': self._generate_order_data,
            'company': self._generate_company_data,
            'address': self._generate_address_data,
            'payment': self._generate_payment_data,
            'review': self._generate_review_data,
            'article': self._generate_article_data
        }
        
        generator_func = generators.get(data_type.lower(), self._generate_user_data)
        
        try:
            data_list = []
            for i in range(count):
                data_list.append(generator_func(i + 1))
            
            return json.dumps(data_list, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"生成 {data_type} 数据时出现错误：{str(e)}"
    
    def _generate_user_data(self, index: int) -> Dict:
        """生成用户数据"""
        return {
            'id': index,
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'name': self.fake.name(),
            'age': random.randint(18, 80),
            'gender': random.choice(['男', '女']),
            'address': self.fake.address(),
            'city': self.fake.city(),
            'country': '中国',
            'registration_date': self.fake.date_between(start_date='-2y', end_date='today').isoformat(),
            'last_login': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
            'is_active': random.choice([True, False]),
            'profile': {
                'bio': self.fake.text(max_nb_chars=200),
                'avatar': self.fake.image_url(),
                'preferences': {
                    'language': random.choice(['zh-CN', 'en-US']),
                    'theme': random.choice(['light', 'dark']),
                    'notifications': random.choice([True, False])
                }
            }
        }
    
    def _generate_product_data(self, index: int) -> Dict:
        """生成产品数据"""
        categories = ['电子产品', '服装', '家居用品', '图书', '食品', '运动用品', '美妆', '玩具']
        
        return {
            'id': index,
            'name': self.fake.catch_phrase() + random.choice(['手机', '电脑', '衣服', '鞋子', '包包']),
            'description': self.fake.text(max_nb_chars=300),
            'category': random.choice(categories),
            'price': round(random.uniform(10.0, 5000.0), 2),
            'original_price': round(random.uniform(10.0, 5000.0), 2),
            'stock': random.randint(0, 1000),
            'sku': f"SKU{index:06d}",
            'brand': self.fake.company(),
            'images': [self.fake.image_url() for _ in range(random.randint(1, 5))],
            'specifications': {
                'weight': f"{random.uniform(0.1, 10.0):.1f}kg",
                'dimensions': f"{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)}cm",
                'color': random.choice(['红色', '蓝色', '黑色', '白色', '绿色']),
                'material': random.choice(['塑料', '金属', '布料', '皮革', '木材'])
            },
            'rating': round(random.uniform(1.0, 5.0), 1),
            'review_count': random.randint(0, 1000),
            'created_at': self.fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'is_available': random.choice([True, False])
        }
    
    def _generate_order_data(self, index: int) -> Dict:
        """生成订单数据"""
        statuses = ['待支付', '已支付', '已发货', '已完成', '已取消', '退款中']
        
        # 生成订单商品
        items = []
        item_count = random.randint(1, 5)
        total_amount = 0
        
        for i in range(item_count):
            price = round(random.uniform(10.0, 500.0), 2)
            quantity = random.randint(1, 3)
            total_amount += price * quantity
            
            items.append({
                'product_id': random.randint(1, 1000),
                'product_name': self.fake.catch_phrase() + '商品',
                'price': price,
                'quantity': quantity,
                'subtotal': price * quantity
            })
        
        return {
            'id': index,
            'order_number': f"ORD{datetime.now().strftime('%Y%m%d')}{index:06d}",
            'user_id': random.randint(1, 1000),
            'user_name': self.fake.name(),
            'items': items,
            'total_amount': round(total_amount, 2),
            'discount_amount': round(random.uniform(0, total_amount * 0.2), 2),
            'final_amount': round(total_amount - random.uniform(0, total_amount * 0.2), 2),
            'status': random.choice(statuses),
            'payment_method': random.choice(['支付宝', '微信支付', '银行卡', '现金']),
            'shipping_address': {
                'name': self.fake.name(),
                'phone': self.fake.phone_number(),
                'address': self.fake.address(),
                'city': self.fake.city(),
                'postal_code': self.fake.postcode()
            },
            'created_at': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
            'payment_at': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat() if random.choice([True, False]) else None,
            'shipped_at': self.fake.date_time_between(start_date='-20d', end_date='now').isoformat() if random.choice([True, False]) else None,
            'delivered_at': self.fake.date_time_between(start_date='-10d', end_date='now').isoformat() if random.choice([True, False]) else None
        }
    
    def _generate_company_data(self, index: int) -> Dict:
        """生成公司数据"""
        return {
            'id': index,
            'name': self.fake.company(),
            'legal_name': self.fake.company() + '有限公司',
            'registration_number': ''.join([str(random.randint(0, 9)) for _ in range(18)]),
            'tax_number': ''.join([str(random.randint(0, 9)) for _ in range(15)]),
            'industry': random.choice(['科技', '制造业', '服务业', '金融', '教育', '医疗', '零售']),
            'address': self.fake.address(),
            'phone': self.fake.phone_number(),
            'email': self.fake.company_email(),
            'website': self.fake.url(),
            'established_date': self.fake.date_between(start_date='-20y', end_date='-1y').isoformat(),
            'employee_count': random.randint(10, 10000),
            'annual_revenue': random.randint(1000000, 1000000000),
            'description': self.fake.text(max_nb_chars=500)
        }
    
    def _generate_address_data(self, index: int) -> Dict:
        """生成地址数据"""
        return {
            'id': index,
            'name': self.fake.name(),
            'phone': self.fake.phone_number(),
            'province': self.fake.province(),
            'city': self.fake.city(),
            'district': self.fake.district(),
            'street': self.fake.street_address(),
            'postal_code': self.fake.postcode(),
            'full_address': self.fake.address(),
            'is_default': random.choice([True, False]),
            'type': random.choice(['家庭', '公司', '学校', '其他'])
        }
    
    def _generate_payment_data(self, index: int) -> Dict:
        """生成支付数据"""
        return {
            'id': index,
            'transaction_id': f"TXN{datetime.now().strftime('%Y%m%d')}{index:08d}",
            'order_id': random.randint(1, 1000),
            'user_id': random.randint(1, 1000),
            'amount': round(random.uniform(1.0, 10000.0), 2),
            'currency': 'CNY',
            'payment_method': random.choice(['支付宝', '微信支付', '银行卡', '信用卡']),
            'status': random.choice(['成功', '失败', '处理中', '已退款']),
            'created_at': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
            'completed_at': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat() if random.choice([True, False]) else None,
            'failure_reason': random.choice(['余额不足', '银行卡过期', '网络错误', None]),
            'refund_amount': round(random.uniform(0, 1000.0), 2) if random.choice([True, False]) else 0
        }
    
    def _generate_review_data(self, index: int) -> Dict:
        """生成评论数据"""
        return {
            'id': index,
            'user_id': random.randint(1, 1000),
            'user_name': self.fake.name(),
            'product_id': random.randint(1, 1000),
            'rating': random.randint(1, 5),
            'title': self.fake.sentence(nb_words=6),
            'content': self.fake.text(max_nb_chars=300),
            'images': [self.fake.image_url() for _ in range(random.randint(0, 3))],
            'helpful_count': random.randint(0, 100),
            'created_at': self.fake.date_time_between(start_date='-180d', end_date='now').isoformat(),
            'is_verified_purchase': random.choice([True, False]),
            'reply': {
                'content': self.fake.text(max_nb_chars=200),
                'created_at': self.fake.date_time_between(start_date='-180d', end_date='now').isoformat()
            } if random.choice([True, False]) else None
        }
    
    def _generate_article_data(self, index: int) -> Dict:
        """生成文章数据"""
        return {
            'id': index,
            'title': self.fake.sentence(nb_words=8),
            'slug': self.fake.slug(),
            'content': self.fake.text(max_nb_chars=2000),
            'summary': self.fake.text(max_nb_chars=200),
            'author_id': random.randint(1, 100),
            'author_name': self.fake.name(),
            'category': random.choice(['科技', '生活', '教育', '娱乐', '体育', '新闻']),
            'tags': [self.fake.word() for _ in range(random.randint(2, 5))],
            'featured_image': self.fake.image_url(),
            'view_count': random.randint(0, 10000),
            'like_count': random.randint(0, 1000),
            'comment_count': random.randint(0, 200),
            'is_published': random.choice([True, False]),
            'created_at': self.fake.date_time_between(start_date='-365d', end_date='now').isoformat(),
            'updated_at': self.fake.date_time_between(start_date='-30d', end_date='now').isoformat()
        } 