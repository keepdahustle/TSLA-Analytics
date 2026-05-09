#!/usr/bin/env python
"""Test script untuk verify API endpoints"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:5000"
ENDPOINTS = [
    "/api/health",
    "/api/stock/latest?days=10",
    "/api/models/evaluation",
    "/api/predictions/sarima",
    "/api/predictions/prophet",
    "/api/predictions/combined",
]

def test_endpoints():
    """Test all API endpoints"""
    print("=" * 60)
    print("TSLA Analytics - API Testing")
    print("=" * 60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Testing {len(ENDPOINTS)} endpoints...\n")
    
    results = {
        "success": 0,
        "failed": 0,
        "endpoints": []
    }
    
    for endpoint in ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"
        try:
            print(f"Testing: {endpoint}...", end=" ")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get("count", "N/A")
                print(f"✓ OK (200) - {count} records")
                results["success"] += 1
                results["endpoints"].append({
                    "endpoint": endpoint,
                    "status": "success",
                    "code": 200
                })
            else:
                print(f"✗ FAILED ({response.status_code})")
                results["failed"] += 1
                results["endpoints"].append({
                    "endpoint": endpoint,
                    "status": "failed",
                    "code": response.status_code
                })
        except requests.exceptions.ConnectionError:
            print(f"✗ CONNECTION ERROR")
            results["failed"] += 1
            results["endpoints"].append({
                "endpoint": endpoint,
                "status": "error",
                "code": "ConnectionError"
            })
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            results["failed"] += 1
            results["endpoints"].append({
                "endpoint": endpoint,
                "status": "error",
                "code": str(type(e).__name__)
            })
        
        sleep(0.5)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {results['success']} passed, {results['failed']} failed")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    try:
        results = test_endpoints()
        exit(0 if results["failed"] == 0 else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
