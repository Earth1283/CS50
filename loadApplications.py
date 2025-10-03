import yaml
import os
from pathlib import Path
from typing import List, Dict
from logger import file_log as fl
from logger import LogLevel

applications: List[Dict] = []

def loadApplications():
    global applications
    applications.clear()
    
    # Get current file path and applications directory
    current_file_path = Path(__file__).resolve()
    base_dir = current_file_path.parent
    apps_dir = base_dir / "applications"
    
    if not apps_dir.exists() or not apps_dir.is_dir():
        fl.warn(f"Applications directory not found at {apps_dir}")
        return
    
    for app_dir in apps_dir.iterdir():
        if not app_dir.is_dir():
            continue
            
        yml_file = app_dir / "application.yml"
        if not yml_file.exists():
            fl.logger(LogLevel.INFO, f"Skipping {app_dir.name}: No application.yml found")
            continue
            
        try:
            with open(yml_file, 'r') as f:
                app_config = yaml.safe_load(f)
        except Exception as e:
            fl.error(f"Error loading {yml_file}: {str(e)}")
            continue

        # Validate required fields
        required_fields = [
            'app_name', 
            'version', 
            'description',
            'author',
            'ready',
            'ready_max_runtime',
            'paralell_ready_process',
            'main'
        ]
        
        if not all(field in app_config for field in required_fields):
            fl.warn(f"Skipping {app_dir.name}: Missing required fields in application.yml")
            continue
            
        # Validate main field structure
        if not isinstance(app_config['main'], list) or len(app_config['main']) != 1:
            fl.warn(f"Skipping {app_dir.name}: 'main' must contain exactly one file")
            continue
            
        # Prepare application metadata
        app_metadata = {
            'name': app_config['app_name'],
            'version': app_config['version'],
            'description': app_config['description'],
            'author': app_config['author'],
            'ready_scripts': app_config['ready'],
            'ready_timeout': app_config['ready_max_runtime'],
            'parallel_ready': app_config['paralell_ready_process'],
            'main_script': app_config['main'][0],
            'directory': str(app_dir),
            'valid': True
        }
        
        applications.append(app_metadata)
        fl.log(f"Loaded application: {app_config['app_name']} v{app_config['version']}")

# Initialize on import
current_file_path = os.path.abspath(__file__)
loadApplications()