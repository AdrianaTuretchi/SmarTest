"""
Script to sanitize Romanian diacritics in templates.json.

This script:
1. Loads assets/json_output/templates.json
2. Applies normalize_ro_diacritics to all template and source_text_for_debug fields
3. Saves the cleaned data back to templates.json
"""
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.text_cleaner import normalize_ro_diacritics


def sanitize_templates():
    """Main function to sanitize templates.json"""
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    
    print("=" * 60)
    print("  SANITIZE TEMPLATES - Romanian Diacritics Cleanup")
    print("=" * 60)
    print(f"\nTemplates file: {templates_path}")
    
    # Check if file exists
    if not templates_path.exists():
        print(f"\n❌ Error: File not found: {templates_path}")
        return
    
    # Load templates
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates = json.load(f)
        print(f"✓ Loaded {len(templates)} templates")
    except Exception as e:
        print(f"\n❌ Error loading file: {e}")
        return
    
    # Sanitize each template
    print("\n🔧 Sanitizing templates...")
    for i, template in enumerate(templates, 1):
        # Normalize the template field
        if 'template' in template:
            original_template = template['template']
            template['template'] = normalize_ro_diacritics(original_template)
            
            # Check if changes were made
            if template['template'] != original_template:
                print(f"  [{i}] {template['id']}: ✓ Template normalized")
        
        # Normalize the source_text_for_debug field
        if 'source_text_for_debug' in template:
            original_debug = template['source_text_for_debug']
            template['source_text_for_debug'] = normalize_ro_diacritics(original_debug)
            
            if template['source_text_for_debug'] != original_debug:
                print(f"  [{i}] {template['id']}: ✓ Debug text normalized")
    
    # Save back to file
    try:
        with open(templates_path, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Successfully saved sanitized templates to: {templates_path}")
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")
        return
    
    print("\n" + "=" * 60)
    print("  SANITIZATION COMPLETE")
    print("=" * 60)
    
    # Show sample
    print("\n📋 Sample (first template):")
    if templates:
        print(f"  ID: {templates[0]['id']}")
        print(f"  Template (first 100 chars): {templates[0]['template'][:100]}...")
    print()


if __name__ == "__main__":
    sanitize_templates()
