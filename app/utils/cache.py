from app import redis_client

def get_stock_level(product_id):
    stock = redis_client.get(f"stock:{product_id}")
    return int(stock) if stock else None

def set_stock_level(product_id, stock):
    redis_client.set(f"stock:{product_id}", stock)
