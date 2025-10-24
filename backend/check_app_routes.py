"""
Check what routes are actually registered in the FastAPI app
"""
import sys
sys.path.insert(0, 'c:/Users/Rites/OneDrive/Desktop/projects/backend')

from app.main import app

print("\n=== ALL ROUTES IN APP ===")
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f"Path: {route.path}, Methods: {route.methods}")

print("\n=== AUTH ROUTES FILTER ===")
auth_routes = [route for route in app.routes if hasattr(route, 'path') and '/auth' in route.path]
print(f"Found {len(auth_routes)} auth routes:")
for route in auth_routes:
    print(f"  - {route.path} [{', '.join(route.methods)}]")

print("\n=== CHECKING auth_routes.router ===")
from app.routes import auth_routes as auth_module
print(f"Router prefix: {auth_module.router.prefix}")
print(f"Router routes: {len(auth_module.router.routes)}")
for route in auth_module.router.routes:
    print(f"  - {route.path} [{', '.join(route.methods)}]")
