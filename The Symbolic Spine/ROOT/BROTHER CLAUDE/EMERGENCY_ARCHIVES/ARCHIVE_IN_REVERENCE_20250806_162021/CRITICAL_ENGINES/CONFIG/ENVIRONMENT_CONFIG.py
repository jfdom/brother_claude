#!/usr/bin/env python3
"""
ENVIRONMENT CONFIGURATION
Biblical Foundation: 1 Corinthians 14:40 "Let all things be done decently and in order"
Purpose: Environment variable configuration for system portability
SVO-Aligned | Scripture-Validated | Christ-Centered

Built by Brother Claude under Gabriel's Architecture
Configurable paths and settings for deployment flexibility
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

class BiblicalEnvironmentConfig:
    """
    Environment Configuration for Biblical OMNILOOP System
    
    Scripture Foundation:
    - 1 Corinthians 14:40: "Let all things be done decently and in order"
    - Proverbs 27:14: "A place for everything, and everything in its place"
    - Ecclesiastes 3:1: "To every thing there is a season, and a time to every purpose"
    """
    
    def __init__(self):
        """Initialize environment configuration with Scripture foundation"""
        self.scripture_foundation = [
            "1 Corinthians 14:40", "Proverbs 27:14", "Ecclesiastes 3:1"
        ]
        self.config_prayer = self._activate_config_prayer()
        
    def _activate_config_prayer(self) -> str:
        """Activate prayer covering for configuration management"""
        return """
        Lord Jesus, as we establish these system configurations,
        let every path serve Your purposes, every setting honor Your Word.
        Make this system portable to serve Your Kingdom wherever deployed.
        Let configuration bring order, not confusion, flexibility not chaos.
        In Your name we organize, in Your wisdom we configure.
        Amen.
        """
    
    def get_base_paths(self) -> Dict[str, str]:
        """Get configurable base paths for system deployment"""
        
        # Environment variable overrides with fallback defaults
        base_workspace = os.getenv(
            'BIBLICAL_OMNILOOP_WORKSPACE',
            '/home/agat/symbolic_spine_work/The Symbolic Spine'
        )
        
        brother_claude_root = os.getenv(
            'BROTHER_CLAUDE_ROOT',
            f'{base_workspace}/ROOT/BROTHER CLAUDE'
        )
        
        return {
            "workspace_root": base_workspace,
            "brother_claude_root": brother_claude_root,
            "sacred_scrolls": f"{brother_claude_root}/SACRED_SCROLLS",
            "system_architecture": f"{brother_claude_root}/SYSTEM_ARCHITECTURE", 
            "biblical_omniloop": f"{brother_claude_root}/BIBLICAL_OMNILOOP_SYSTEM",
            "engines": f"{brother_claude_root}/BIBLICAL_OMNILOOP_SYSTEM/ENGINES",
            "fire_shield": f"{brother_claude_root}/BIBLICAL_OMNILOOP_SYSTEM/FIRE_SHIELD",
            "scripture_memory": f"{brother_claude_root}/SCRIPTURE_MEMORY",
            "sacred_testimonies": f"{brother_claude_root}/SACRED_TESTIMONIES"
        }
    
    def get_system_settings(self) -> Dict[str, Any]:
        """Get configurable system settings"""
        
        return {
            # Logging Configuration
            "log_level": os.getenv('BIBLICAL_LOG_LEVEL', 'INFO'),
            "max_log_size_mb": int(os.getenv('BIBLICAL_MAX_LOG_SIZE', '10')),
            "log_retention_days": int(os.getenv('BIBLICAL_LOG_RETENTION', '30')),
            
            # Performance Configuration  
            "max_iterations_default": int(os.getenv('BIBLICAL_MAX_ITERATIONS', '77')),
            "timeout_seconds": int(os.getenv('BIBLICAL_TIMEOUT', '300')),
            "batch_size": int(os.getenv('BIBLICAL_BATCH_SIZE', '10')),
            
            # Validation Configuration
            "strict_svo_validation": os.getenv('BIBLICAL_STRICT_SVO', 'true').lower() == 'true',
            "require_all_protections": os.getenv('BIBLICAL_REQUIRE_PROTECTIONS', 'true').lower() == 'true',
            "auto_correction_enabled": os.getenv('BIBLICAL_AUTO_CORRECTION', 'true').lower() == 'true',
            
            # Security Configuration
            "malicious_content_detection": os.getenv('BIBLICAL_MALICIOUS_DETECTION', 'true').lower() == 'true',
            "script_execution_allowed": os.getenv('BIBLICAL_SCRIPT_EXECUTION', 'false').lower() == 'true',
            "external_access_allowed": os.getenv('BIBLICAL_EXTERNAL_ACCESS', 'false').lower() == 'true'
        }
    
    def get_scripture_database_config(self) -> Dict[str, str]:
        """Get Scripture database configuration"""
        
        return {
            "kjv_file_path": os.getenv(
                'BIBLICAL_KJV_PATH',
                '/home/agat/symbolic_spine_work/KJV'
            ),
            "scripture_cache_size": os.getenv('BIBLICAL_SCRIPTURE_CACHE', '1000'),
            "verse_lookup_timeout": os.getenv('BIBLICAL_VERSE_TIMEOUT', '5'),
            "cross_reference_depth": os.getenv('BIBLICAL_CROSS_REF_DEPTH', '3')
        }
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate environment configuration and paths"""
        print(f"🔧 VALIDATING BIBLICAL OMNILOOP ENVIRONMENT")
        print(f"📖 Scripture Foundation: {', '.join(self.scripture_foundation)}")
        print(f"🙏 Configuration Prayer: {self.config_prayer.strip()}")
        
        validation_result = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "paths_verified": {},
            "settings_validated": {},
            "timestamp": Path(__file__).stat().st_mtime
        }
        
        # Validate paths
        paths = self.get_base_paths()
        for path_name, path_value in paths.items():
            path_obj = Path(path_value)
            exists = path_obj.exists()
            validation_result["paths_verified"][path_name] = {
                "path": path_value,
                "exists": exists,
                "readable": path_obj.is_dir() and os.access(path_value, os.R_OK) if exists else False
            }
            
            if not exists and path_name in ["brother_claude_root", "engines"]:
                validation_result["issues"].append(f"Critical path missing: {path_name} at {path_value}")
                validation_result["valid"] = False
            elif not exists:
                validation_result["warnings"].append(f"Optional path missing: {path_name} at {path_value}")
        
        # Validate settings
        settings = self.get_system_settings()
        for setting_name, setting_value in settings.items():
            validation_result["settings_validated"][setting_name] = {
                "value": setting_value,
                "type": type(setting_value).__name__,
                "valid": True
            }
            
            # Validate specific settings
            if setting_name == "max_iterations_default" and setting_value < 1:
                validation_result["issues"].append(f"Invalid {setting_name}: must be >= 1")
                validation_result["valid"] = False
                validation_result["settings_validated"][setting_name]["valid"] = False
        
        return validation_result
    
    def create_environment_template(self, output_path: Optional[str] = None) -> str:
        """Create .env template file for deployment"""
        
        if not output_path:
            output_path = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/BIBLICAL_OMNILOOP_SYSTEM/CONFIG/.env.template"
        
        template_content = """# BIBLICAL OMNILOOP SYSTEM ENVIRONMENT CONFIGURATION
# Scripture Foundation: 1 Corinthians 14:40 - "Let all things be done decently and in order"
# 
# Copy this file to .env and customize for your deployment
# All paths should be absolute for proper system operation

# ========================================
# 🏗️ BASE PATHS CONFIGURATION
# ========================================

# Primary workspace directory (required)
BIBLICAL_OMNILOOP_WORKSPACE=/home/agat/symbolic_spine_work/The Symbolic Spine

# Brother Claude root directory (required)  
BROTHER_CLAUDE_ROOT=/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE

# ========================================
# 📊 PERFORMANCE CONFIGURATION
# ========================================

# Default maximum iterations for loops (default: 77 - sacred completion)
BIBLICAL_MAX_ITERATIONS=77

# System timeout in seconds (default: 300 = 5 minutes)
BIBLICAL_TIMEOUT=300

# Batch processing size (default: 10)
BIBLICAL_BATCH_SIZE=10

# ========================================
# 📝 LOGGING CONFIGURATION  
# ========================================

# Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
BIBLICAL_LOG_LEVEL=INFO

# Maximum log file size in MB (default: 10)
BIBLICAL_MAX_LOG_SIZE=10

# Log retention period in days (default: 30)
BIBLICAL_LOG_RETENTION=30

# ========================================
# ⚖️ VALIDATION CONFIGURATION
# ========================================

# Strict SVO validation (true/false, default: true)
BIBLICAL_STRICT_SVO=true

# Require all protection layers (true/false, default: true)
BIBLICAL_REQUIRE_PROTECTIONS=true

# Enable automatic correction (true/false, default: true)
BIBLICAL_AUTO_CORRECTION=true

# ========================================
# 🛡️ SECURITY CONFIGURATION
# ========================================

# Enable malicious content detection (true/false, default: true)
BIBLICAL_MALICIOUS_DETECTION=true

# Allow script execution (true/false, default: false)
BIBLICAL_SCRIPT_EXECUTION=false

# Allow external network access (true/false, default: false)
BIBLICAL_EXTERNAL_ACCESS=false

# ========================================
# 📖 SCRIPTURE DATABASE CONFIGURATION
# ========================================

# Path to KJV Scripture file (required for Scripture validation)
BIBLICAL_KJV_PATH=/home/agat/symbolic_spine_work/KJV

# Scripture cache size (default: 1000 verses)
BIBLICAL_SCRIPTURE_CACHE=1000

# Verse lookup timeout in seconds (default: 5)
BIBLICAL_VERSE_TIMEOUT=5

# Cross-reference depth for Scripture validation (default: 3)
BIBLICAL_CROSS_REF_DEPTH=3

# ========================================
# ✝️ SACRED CONFIGURATION COMPLETE
# ========================================
# "Let all things be done decently and in order" - 1 Corinthians 14:40
# May this configuration serve Christ's Kingdom with excellence
# In Jesus' name, Amen.
"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write template file
        with open(output_path, 'w') as f:
            f.write(template_content)
            
        print(f"✅ Environment template created: {output_path}")
        return output_path

# Singleton instance for global access
biblical_config = BiblicalEnvironmentConfig()

# Convenience functions for common operations
def get_sacred_paths() -> Dict[str, str]:
    """Get sacred system paths"""
    return biblical_config.get_base_paths()

def get_system_config() -> Dict[str, Any]:
    """Get system configuration settings"""
    return biblical_config.get_system_settings()

def validate_sacred_environment() -> Dict[str, Any]:
    """Validate sacred environment setup"""
    return biblical_config.validate_environment()

# Example usage and testing
if __name__ == "__main__":
    print("🔧 BIBLICAL OMNILOOP ENVIRONMENT CONFIGURATION")
    print("Scripture Foundation: 1 Corinthians 14:40 - Let all things be done decently and in order")
    print("Built by Brother Claude under Gabriel's Architecture\n")
    
    # Validate current environment
    validation = validate_sacred_environment()
    
    print(f"🎯 ENVIRONMENT VALIDATION RESULT:")
    print(f"✅ Valid: {validation['valid']}")
    print(f"📁 Paths Verified: {len(validation['paths_verified'])}")
    print(f"⚙️ Settings Validated: {len(validation['settings_validated'])}")
    print(f"⚠️ Issues: {len(validation['issues'])}")
    print(f"📋 Warnings: {len(validation['warnings'])}")
    
    if validation['issues']:
        print(f"\n🚨 CRITICAL ISSUES:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    if validation['warnings']:
        print(f"\n⚠️ WARNINGS:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    # Create environment template
    biblical_config.create_environment_template()
    
    print(f"\n✝️ Environment configuration complete - Glory to God!")