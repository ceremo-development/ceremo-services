#!/usr/bin/env python3
"""
Health check script for Ceremo Services
"""
import sys
import requests
from typing import Dict, Any, Tuple


def check_service_health(base_url: str) -> Tuple[bool, Dict[str, Any]]:
    """Check if the service is healthy"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, {"error": f"Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}


def check_mysql_connection(base_url: str) -> Tuple[bool, str]:
    """Check if MySQL is accessible by trying to fetch users"""
    try:
        response = requests.get(
            f"{base_url}/api/users/search?email=test@test.com", timeout=5
        )
        # 404 is ok, means DB is accessible
        if response.status_code in [200, 404]:
            return True, "MySQL database is accessible"
        return False, f"Unexpected status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Failed to connect to MySQL: {str(e)}"


def check_database_health(base_url: str) -> Tuple[bool, str]:
    """Check database health endpoint if available"""
    try:
        response = requests.get(f"{base_url}/health/database", timeout=5)
        if response.status_code == 200:
            return True, "Database health check passed"
        return False, f"Database health check failed: {response.status_code}"
    except requests.exceptions.RequestException:
        # If endpoint doesn't exist, fallback to connection test
        return check_mysql_connection(base_url)


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"

    print(f"Running health checks for Ceremo Services: {base_url}\n")

    # Check service health
    print("1. Checking service health...")
    is_healthy, health_data = check_service_health(base_url)
    if is_healthy:
        print("   ✓ Ceremo service is healthy")
        print(f"   - Environment: {health_data.get('environment', 'unknown')}")
        print(f"   - Status: {health_data.get('status', 'unknown')}")
        print(f"   - Database: {health_data.get('database', 'unknown')}")
    else:
        error_msg = health_data.get("error", "Unknown error")
        print(f"   ✗ Ceremo service is unhealthy: {error_msg}")
        sys.exit(1)

    # Check MySQL connection
    print("\n2. Checking MySQL database connection...")
    db_ok, db_msg = check_database_health(base_url)
    if db_ok:
        print(f"   ✓ {db_msg}")
    else:
        print(f"   ✗ {db_msg}")
        sys.exit(1)

    print("\n✓ All health checks passed!")
    print("   - Ceremo application is running correctly")
    print("   - MySQL database (ceremo_db) is accessible")
    print("   - Ready to handle requests")
    sys.exit(0)


if __name__ == "__main__":
    main()
