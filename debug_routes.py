"""
Debug script to find why auth_routes is not loading in uvicorn
"""
import sys
import traceback

sys.path.insert(0, 'c:/Users/Rites/OneDrive/Desktop/projects/backend')

print("=" * 60)
print("STEP 1: Testing auth_routes import")
print("=" * 60)

try:
    from app.routes import auth_routes
    print("✅ auth_routes imported successfully")
    print(f"   Router: {auth_routes.router}")
    print(f"   Routes count: {len(auth_routes.router.routes)}")
    for route in auth_routes.router.routes:
        print(f"   - {route.path}")
except Exception as e:
    print(f"❌ FAILED to import auth_routes!")
    print(f"   Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("STEP 2: Testing FastAPI app creation")
print("=" * 60)

try:
    from app.main import app
    print("✅ FastAPI app created successfully")
    
    # Check all routes
    auth_routes_found = [r for r in app.routes if hasattr(r, 'path') and '/api/auth' in r.path]
    
    print(f"\n📊 Total routes in app: {len([r for r in app.routes if hasattr(r, 'path')])}")
    print(f"📊 Auth routes found: {len(auth_routes_found)}")
    
    if auth_routes_found:
        print("\n✅ Auth routes ARE registered:")
        for r in auth_routes_found:
            print(f"   - {r.path} [{','.join(r.methods) if hasattr(r, 'methods') else 'N/A'}]")
    else:
        print("\n❌ NO AUTH ROUTES in FastAPI app!")
        print("\nAll routes:")
        for r in app.routes:
            if hasattr(r, 'path'):
                print(f"   - {r.path}")
                
except Exception as e:
    print(f"❌ FAILED to create FastAPI app!")
    print(f"   Error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
print("If you see this, the code is fine!")
print("Problem is ONLY in running uvicorn server.")
