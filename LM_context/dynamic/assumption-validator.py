#!/usr/bin/env python3
"""
Assumption Validator for Project

This script validates project assumptions and hypotheses.
Customize the validation methods for your specific project needs.
"""

import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class AssumptionValidator:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "errors": []
            }
        }
        
    def validate_environment(self):
        """Validate basic development environment."""
        print("🔍 Validating development environment...")
        
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major >= 3 and python_version.minor >= 7:
                self.record_result("python_version", True, f"Python {python_version.major}.{python_version.minor}")
            else:
                self.record_result("python_version", False, f"Python version too old: {python_version}")
                
            # Check project directory structure
            context_dir = Path(__file__).parent.parent
            required_dirs = ["static", "evolving", "dynamic", "archive"]
            
            for dir_name in required_dirs:
                dir_path = context_dir / dir_name
                if dir_path.exists():
                    self.record_result(f"directory_{dir_name}", True, f"Directory exists: {dir_name}")
                else:
                    self.record_result(f"directory_{dir_name}", False, f"Missing directory: {dir_name}")
                    
            return True
            
        except Exception as e:
            self.record_result("environment_validation", False, f"Error: {str(e)}")
            return False
            
    def validate_project_specific(self):
        """
        CUSTOMIZE THIS METHOD for your specific project validations.
        
        Examples:
        - Test API connectivity
        - Verify database connections
        - Check hardware availability
        - Validate configuration files
        - Test build processes
        """
        print("🔍 Validating project-specific requirements...")
        
        try:
            # Example validation - customize for your project
            self.record_result("project_setup", True, "Project setup validation placeholder")
            
            # Add your specific validations here:
            # - Hardware checks
            # - Network connectivity
            # - Service availability
            # - Configuration validation
            # - Build system checks
            
            return True
            
        except Exception as e:
            self.record_result("project_validation", False, f"Error: {str(e)}")
            return False
            
    def record_result(self, test_name, passed, details):
        """Record a validation result."""
        self.results["validations"][test_name] = {
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results["summary"]["total"] += 1
        if passed:
            self.results["summary"]["passed"] += 1
            print(f"  ✅ {test_name}: {details}")
        else:
            self.results["summary"]["failed"] += 1
            self.results["summary"]["errors"].append(f"{test_name}: {details}")
            print(f"  ❌ {test_name}: {details}")
            
    def run_health_check(self):
        """Run basic health check validations."""
        print("🏥 Running health check...")
        
        success = True
        success &= self.validate_environment()
        
        return success
        
    def run_full_validation(self):
        """Run complete validation suite."""
        print("🔬 Running full validation suite...")
        
        success = True
        success &= self.validate_environment()
        success &= self.validate_project_specific()
        
        return success
        
    def save_results(self):
        """Save validation results to file."""
        results_file = Path(__file__).parent / "validation-results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📊 Results saved to: {results_file}")
        
    def print_summary(self):
        """Print validation summary."""
        summary = self.results["summary"]
        print("\n📋 Validation Summary:")
        print(f"  Total tests: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        
        if summary["errors"]:
            print("\n❌ Errors:")
            for error in summary["errors"]:
                print(f"  - {error}")
        else:
            print("\n✅ All validations passed!")

def main():
    parser = argparse.ArgumentParser(description="Validate project assumptions and environment")
    parser.add_argument("--health-check", action="store_true", help="Run basic health check only")
    parser.add_argument("--quick-check", action="store_true", help="Run quick validation")
    parser.add_argument("--save-results", action="store_true", help="Save results to file")
    
    args = parser.parse_args()
    
    validator = AssumptionValidator()
    
    try:
        if args.health_check or args.quick_check:
            success = validator.run_health_check()
        else:
            success = validator.run_full_validation()
            
        validator.print_summary()
        
        if args.save_results:
            validator.save_results()
            
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Validation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
