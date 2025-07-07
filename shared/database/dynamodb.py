"""
DynamoDB service for the platform
"""
import os
import boto3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from shared.models.base import BaseUser, Shop, Product, Order, Review, Address


class DynamoDBService:
    def __init__(self):
        # Read config from environment
        region = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")
        env = os.getenv("ENVIRONMENT", "production")

        # Use endpoint_url only for local development
        if env == "development" and endpoint_url:
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=endpoint_url,
                region_name=region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        else:
            # For AWS, use region and credentials if provided, else use default provider chain
            session_kwargs = {"region_name": region}
            if aws_access_key_id and aws_secret_access_key:
                session_kwargs["aws_access_key_id"] = aws_access_key_id
                session_kwargs["aws_secret_access_key"] = aws_secret_access_key
            self.dynamodb = boto3.resource('dynamodb', **session_kwargs)
        
        # Table names
        self.users_table = self.dynamodb.Table('BaseUser')
        self.shops_table = self.dynamodb.Table('shops')
        self.products_table = self.dynamodb.Table('Product')
        self.orders_table = self.dynamodb.Table('Order')
        self.reviews_table = self.dynamodb.Table('reviews')
        self.addresses_table = self.dynamodb.Table('addresses')
    
    def _serialize_datetime(self, obj):
        """Convert datetime objects to ISO string for DynamoDB"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    def _deserialize_datetime(self, data: Dict) -> Dict:
        """Convert ISO strings back to datetime objects"""
        for key, value in data.items():
            if isinstance(value, str) and 'T' in value and value.endswith('Z'):
                try:
                    data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    pass
        return data
    
    # User operations
    async def create_user(self, user: BaseUser) -> Dict:
        """Create a new user"""
        user_data = user.dict()
        user_data = {k: self._serialize_datetime(v) for k, v in user_data.items()}
        
        self.users_table.put_item(Item=user_data)
        return user_data
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        response = self.users_table.get_item(Key={'user_id': user_id})
        print(response)
        if 'Item' in response:
            return self._deserialize_datetime(response['Item'])
        
        return None
    
    async def update_user(self, user_id: str, updates: Dict) -> Optional[Dict]:
        """Update user data"""
        update_expression = "SET "
        expression_values = {}
        
        for key, value in updates.items():
            if key != 'user_id':
                update_expression += f"#{key} = :{key}, "
                expression_values[f":{key}"] = self._serialize_datetime(value)
                expression_values[f"#{key}"] = key
        
        update_expression = update_expression.rstrip(", ")
        
        response = self.users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames={v: k for k, v in expression_values.items() if k.startswith('#')},
            ReturnValues="ALL_NEW"
        )
        
        if 'Attributes' in response:
            return self._deserialize_datetime(response['Attributes'])
        return None
    
    # Shop operations
    async def create_shop(self, shop: Shop) -> Dict:
        """Create a new shop"""
        shop_data = shop.dict()
        shop_data = {k: self._serialize_datetime(v) for k, v in shop_data.items()}
        
        self.shops_table.put_item(Item=shop_data)
        return shop_data
    
    async def get_shop(self, shop_id: str) -> Optional[Dict]:
        """Get shop by ID"""
        response = self.shops_table.get_item(Key={'shop_id': shop_id})
        if 'Item' in response:
            return self._deserialize_datetime(response['Item'])
        return None
    
    async def get_shops_by_merchant(self, merchant_id: str) -> List[Dict]:
        """Get all shops for a merchant"""
        response = self.shops_table.query(
            IndexName='merchant_id-index',
            KeyConditionExpression=Key('merchant_id').eq(merchant_id)
        )
        
        shops = []
        for item in response.get('Items', []):
            shops.append(self._deserialize_datetime(item))
        
        return shops
    
    async def get_approved_shops(self, category: Optional[str] = None) -> List[Dict]:
        """Get all approved shops, optionally filtered by category"""
        if category:
            response = self.shops_table.scan(
                FilterExpression=Attr('status').eq('approved') & Attr('category').eq(category)
            )
        else:
            response = self.shops_table.scan(
                FilterExpression=Attr('status').eq('approved')
            )
        
        shops = []
        for item in response.get('Items', []):
            shops.append(self._deserialize_datetime(item))
        
        return shops
    
    async def update_shop_status(self, shop_id: str, status: str) -> Optional[Dict]:
        """Update shop approval status"""
        response = self.shops_table.update_item(
            Key={'shop_id': shop_id},
            UpdateExpression="SET #status = :status, #updated_at = :updated_at",
            ExpressionAttributeValues={
                ':status': status,
                ':updated_at': self._serialize_datetime(datetime.utcnow())
            },
            ExpressionAttributeNames={
                '#status': 'status',
                '#updated_at': 'updated_at'
            },
            ReturnValues="ALL_NEW"
        )
        
        if 'Attributes' in response:
            return self._deserialize_datetime(response['Attributes'])
        return None
    
    # Product operations
    async def create_product(self, product: Product) -> Dict:
        """Create a new product"""
        product_data = product.dict()
        product_data = {k: self._serialize_datetime(v) for k, v in product_data.items()}
        
        self.products_table.put_item(Item=product_data)
        return product_data
    
    async def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        response = self.products_table.get_item(Key={'product_id': product_id})
        if 'Item' in response:
            return self._deserialize_datetime(response['Item'])
        return None
    
    async def get_products_by_shop(self, shop_id: str) -> List[Dict]:
        """Get all products for a shop"""
        response = self.products_table.query(
            IndexName='shop_id-index',
            KeyConditionExpression=Key('shop_id').eq(shop_id)
        )
        
        products = []
        for item in response.get('Items', []):
            products.append(self._deserialize_datetime(item))
        
        return products
    
    # Order operations
    async def create_order(self, order: Order) -> Dict:
        """Create a new order"""
        order_data = order.dict()
        order_data = {k: self._serialize_datetime(v) for k, v in order_data.items()}
        
        self.orders_table.put_item(Item=order_data)
        return order_data
    
    async def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        response = self.orders_table.get_item(Key={'order_id': order_id})
        if 'Item' in response:
            return self._deserialize_datetime(response['Item'])
        return None
    
    async def get_orders_by_customer(self, customer_id: str) -> List[Dict]:
        """Get all orders for a customer"""
        response = self.orders_table.query(
            IndexName='customer_id-index',
            KeyConditionExpression=Key('customer_id').eq(customer_id)
        )
        
        orders = []
        for item in response.get('Items', []):
            orders.append(self._deserialize_datetime(item))
        
        return orders
    
    async def get_orders_by_shop(self, shop_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get all orders for a shop, optionally filtered by status"""
        if status:
            response = self.orders_table.query(
                IndexName='shop_id-index',
                KeyConditionExpression=Key('shop_id').eq(shop_id),
                FilterExpression=Attr('status').eq(status)
            )
        else:
            response = self.orders_table.query(
                IndexName='shop_id-index',
                KeyConditionExpression=Key('shop_id').eq(shop_id)
            )
        
        orders = []
        for item in response.get('Items', []):
            orders.append(self._deserialize_datetime(item))
        
        return orders
    
    async def update_order_status(self, order_id: str, status: str) -> Optional[Dict]:
        """Update order status"""
        response = self.orders_table.update_item(
            Key={'order_id': order_id},
            UpdateExpression="SET #status = :status, #updated_at = :updated_at",
            ExpressionAttributeValues={
                ':status': status,
                ':updated_at': self._serialize_datetime(datetime.utcnow())
            },
            ExpressionAttributeNames={
                '#status': 'status',
                '#updated_at': 'updated_at'
            },
            ReturnValues="ALL_NEW"
        )
        
        if 'Attributes' in response:
            return self._deserialize_datetime(response['Attributes'])
        return None


# Global instance
db_service = DynamoDBService() 
