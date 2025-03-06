from app import redis_client
import json

# Stock level caching
def get_stock_level(product_id):
    stock = redis_client.get(f"stock:{product_id}")
    return int(stock) if stock else None

def set_stock_level(product_id, stock, min_stock_level=None):
    redis_client.set(f"stock:{product_id}", stock)
    
    # Set alert if stock level is below threshold
    if min_stock_level is not None and stock < min_stock_level:
        set_low_stock_alert(product_id)
    else:
        clear_low_stock_alert(product_id)

# Low stock alerts
def set_low_stock_alert(product_id):
    redis_client.sadd("low_stock_alerts", product_id)

def clear_low_stock_alert(product_id):
    redis_client.srem("low_stock_alerts", product_id)

def get_low_stock_alerts():
    return [int(pid) for pid in redis_client.smembers("low_stock_alerts")]

# Cache product details
def cache_product(product):
    redis_client.setex(
        f"product:{product.id}", 
        3600,  # Cache for 1 hour
        json.dumps(product.to_dict())
    )

def get_cached_product(product_id):
    data = redis_client.get(f"product:{product_id}")
    return json.loads(data) if data else None

# Cache warehouse details
def cache_warehouse(warehouse):
    redis_client.setex(
        f"warehouse:{warehouse.id}", 
        3600,  # Cache for 1 hour
        json.dumps(warehouse.to_dict())
    )

def get_cached_warehouse(warehouse_id):
    data = redis_client.get(f"warehouse:{warehouse_id}")
    return json.loads(data) if data else None