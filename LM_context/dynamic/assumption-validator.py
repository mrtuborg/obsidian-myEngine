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
        """Validate Obsidian Engine-specific requirements."""
        print("🔍 Validating Obsidian Engine requirements...")
        
        try:
            success = True
            
            # Check Scripts directory and JavaScript components
            success &= self.validate_scripts_directory()
            
            # Check Templates directory
            success &= self.validate_templates_directory()
            
            # Check TestSuite directory
            success &= self.validate_test_suite()
            
            # Validate project structure
            success &= self.validate_obsidian_structure()
            
            return success
            
        except Exception as e:
            self.record_result("project_validation", False, f"Error: {str(e)}")
            return False
            
    def validate_scripts_directory(self):
        """Validate Scripts directory and JavaScript components."""
        try:
            project_root = Path(__file__).parent.parent.parent
            scripts_dir = project_root / "Scripts"
            
            if not scripts_dir.exists():
                self.record_result("scripts_directory", False, "Scripts directory not found")
                return False
                
            self.record_result("scripts_directory", True, "Scripts directory exists")
            
            # Check for core JavaScript files
            required_scripts = [
                "dailyNoteComposer.js",
                "activityComposer.js",
                "components/noteBlocksParser.js",
                "components/todoRollover.js",
                "components/mentionsProcessor.js",
                "components/activitiesInProgress.js",
                "utilities/fileIO.js"
            ]
            
            for script in required_scripts:
                script_path = scripts_dir / script
                if script_path.exists():
                    self.record_result(f"script_{script.replace('/', '_').replace('.js', '')}", True, f"Found {script}")
                else:
                    self.record_result(f"script_{script.replace('/', '_').replace('.js', '')}", False, f"Missing {script}")
                    
            return True
            
        except Exception as e:
            self.record_result("scripts_validation", False, f"Scripts validation error: {str(e)}")
            return False
            
    def validate_templates_directory(self):
        """Validate Templates directory."""
        try:
            project_root = Path(__file__).parent.parent.parent
            templates_dir = project_root / "Templates"
            
            if not templates_dir.exists():
                self.record_result("templates_directory", False, "Templates directory not found")
                return False
                
            self.record_result("templates_directory", True, "Templates directory exists")
            
            # Check for required templates
            required_templates = [
                "DailyNote-template.md",
                "Activity-template.md"
            ]
            
            for template in required_templates:
                template_path = templates_dir / template
                if template_path.exists():
                    self.record_result(f"template_{template.replace('-', '_').replace('.md', '')}", True, f"Found {template}")
                else:
                    self.record_result(f"template_{template.replace('-', '_').replace('.md', '')}", False, f"Missing {template}")
                    
            return True
            
        except Exception as e:
            self.record_result("templates_validation", False, f"Templates validation error: {str(e)}")
            return False
            
    def validate_test_suite(self):
        """Validate TestSuite directory."""
        try:
            project_root = Path(__file__).parent.parent.parent
            test_dir = project_root / "TestSuite"
            
            if not test_dir.exists():
                self.record_result("test_suite_directory", False, "TestSuite directory not found")
                return False
                
            self.record_result("test_suite_directory", True, "TestSuite directory exists")
            
            # Check for test categories
            test_categories = ["Core", "Features", "Integration", "Samples"]
            
            for category in test_categories:
                category_path = test_dir / category
                if category_path.exists():
                    self.record_result(f"test_category_{category.lower()}", True, f"Found {category} tests")
                else:
                    self.record_result(f"test_category_{category.lower()}", False, f"Missing {category} tests")
                    
            return True
            
        except Exception as e:
            self.record_result("test_suite_validation", False, f"TestSuite validation error: {str(e)}")
            return False
            
    def validate_obsidian_structure(self):
        """Validate expected Obsidian vault structure."""
        try:
            project_root = Path(__file__).parent.parent.parent
            
            # Check for knowledge directory
            knowledge_dir = project_root / "knowledge"
            if knowledge_dir.exists():
                self.record_result("knowledge_directory", True, "Knowledge directory exists")
            else:
                self.record_result("knowledge_directory", False, "Knowledge directory not found")
                
            # Check for minds-vault submodule
            minds_vault_dir = project_root / "minds-vault"
            if minds_vault_dir.exists():
                self.record_result("minds_vault_submodule", True, "minds-vault submodule exists")
            else:
                self.record_result("minds_vault_submodule", False, "minds-vault submodule not found")
                
            # Check for README files
            readme_files = ["README.md", "README_journal_backup.md", "README_PDF_CONVERTER.md"]
            for readme in readme_files:
                readme_path = project_root / readme
                if readme_path.exists():
                    self.record_result(f"readme_{readme.replace('.md', '').replace('_', '_').lower()}", True, f"Found {readme}")
                else:
                    self.record_result(f"readme_{readme.replace('.md', '').replace('_', '_').lower()}", False, f"Missing {readme}")
                    
            return True
            
        except Exception as e:
            self.record_result("obsidian_structure_validation", False, f"Structure validation error: {str(e)}")
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
