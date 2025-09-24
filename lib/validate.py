"""
validate.py - Validate resume.yaml agains schema.json
"""

import argparse # For parsing command-line options
import sys # For command line arguments
import json # For loading JSON schema
import yaml # For loading YAML resume
import logging # For logging errors and info
from jsonschema import validate, ValidationError # For validating JSON against schema
from pathlib import Path # For file path operations
from colorama import init, Fore # For colored terminal output

# Initialize colorama and enable reset styles after each print
init(autoreset=True)

print(f"{Fore.BLUE}➡️️  Starting: Validating YAML data")

# Configure logging for better error messages and info
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_yaml(yaml_path: Path) -> dict:
    """
    Load data from a YAML file.
    Args:
        yaml_path (Path): The path to the YAML file.
    Returns:
        dict: The loaded YAML data.
    """
    try:
        with yaml_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load YAML file {yaml_path}: {e}")
        raise

def load_json(json_path: Path) -> dict:
    """
    Load data from a JSON file.
    Args:
        json_path (Path): The path to the JSON file.
    Returns:
        dict: The loaded JSON data.
    """
    try:
        with json_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to load JSON file {json_path}: {e}")
        raise

def validate_yaml_against_schema(yaml_data: dict, schema: dict) -> None:
    """
    Validate YAML data against a JSON schema.
    Args:
        yaml_data (dict): The YAML data to validate.
        schema (dict): The JSON schema to validate against.
    Raises:
        ValidationError: If the YAML data does not conform to the schema.
    """
    try:
        validate(instance=yaml_data, schema=schema)
        logger.info("YAML data is valid against the JSON schema")
    except ValidationError as e:
        logger.error(f"YAML data validation error: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Validate a YAML file against a JSON schema and check Jinja template syntax.")
    parser.add_argument('--resume', required=True, help="Path to the YAML resume file")
    parser.add_argument('--schema', required=True, help="Path to the JSON schema file")

    args = parser.parse_args()

    resume_path = Path(args.resume)
    schema_path = Path(args.schema)

    if not resume_path.is_file():
        logger.error(f"Resume file not found: {resume_path}")
        print(f"{Fore.RED}❌ Error: Resume file not found '{resume_path}'")
        sys.exit(1)

    if not schema_path.is_file():
        logger.error(f"Schema file not found: {schema_path}")
        print(f"{Fore.RED}❌ Error: Schema file not found '{schema_path}'")
        sys.exit(1)

    try:
        yaml_data = load_yaml(resume_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Error loading YAML file: {e}")
        sys.exit(1)
    
    try:
        schema = load_json(schema_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Error loading JSON file: {e}")
        sys.exit(1)
    
    try:
        validate_yaml_against_schema(yaml_data, schema)
    except ValidationError:
        print(f"{Fore.RED}❌ YAML data is invalid against the schema: {e}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✅ All validations passed successfully.")

if __name__ == '__main__':
    main()