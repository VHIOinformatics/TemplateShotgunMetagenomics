#!/usr/bin/env python3
"""
Automatic RMarkdown report generator from YAML configuration files.

Usage:
    python generate_rmd.py config.yml template.rmd

This script:
1. Reads YAML configuration
2. Reads RMarkdown template with Jinja2
3. Renders template with YAML values
4. Generates final RMarkdown file
"""

import sys
import yaml
import argparse
from pathlib import Path
from jinja2 import FileSystemLoader, Environment, StrictUndefined
from datetime import datetime
from typing import Any, Dict, Optional


def load_config(config_path):
    """Load YAML configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"✓ Configuration loaded from: {config_path}")
        return config
    except FileNotFoundError:
        print(f"✗ Error: Configuration file not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"✗ Error parsing YAML: {e}")
        sys.exit(1)


def load_template(template_path):
    """Load Jinja2 template from file."""
    try:
        template_path = Path(template_path)
        if not template_path.exists():
            raise FileNotFoundError(template_path)

        # Use FileSystemLoader so templates can `include` or `import` other files
        loader = FileSystemLoader(str(template_path.parent))
        env = Environment(
            loader=loader,
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )

        template = env.get_template(template_path.name)
        print(f"✓ Template loaded from: {template_path}")
        return template
    except FileNotFoundError:
        print(f"✗ Error: Template file not found: {template_path}")
        sys.exit(1)


def process_date(date_config):
    """Process date configuration."""
    # Accept None, 'auto', datetime instances, or a literal string
    if date_config is None:
        return ''
    if isinstance(date_config, datetime):
        return date_config.strftime('%d %b %Y')
    if str(date_config).lower() == 'auto':
        return "`r format(Sys.time(), '%d %b %Y')`"
    # Return as a plain string
    return str(date_config)


def render_rmd(template, config):
    """Render RMarkdown template with configuration values."""
    # Ensure metadata exists and process date
    metadata = config.get('metadata', {}) or {}
    metadata_date = metadata.get('date')
    metadata['date_rendered'] = process_date(metadata_date)
    config['metadata'] = metadata
    
    # Prepare context for Jinja2
    context = {
        'metadata': config.get('metadata', {}),
        'project_info': config.get('project_info', {}),
        'background': config.get('background', ''),
        'samples_info': config.get('samples_info', ''),
        'feature_columns': config.get('feature_columns', []),
        'analyses': config.get('analyses', {}),
        'filtering': config.get('filtering', {}),
        'normalization': config.get('normalization', {}),
        'references': config.get('references', ''),
        'input_files': config.get('input_files', {}),
        'mode': config.get('mode', {}),
        'metadata_source': config.get('metadata_source', {}),
        'output': config.get('output', {}),
    }
    
    try:
        rendered = template.render(**context)
        print("✓ Template rendered successfully")
        return rendered
    except Exception as e:
        print(f"✗ Error rendering template: {e}")
        sys.exit(1)


def save_rmd(content, output_path):
    """Save content to RMarkdown file."""
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ RMarkdown file generated: {output_path}")
        print(f"  Size: {len(content)} characters")
        return output_path
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        sys.exit(1)


def main():
    """Main function."""
    
    parser = argparse.ArgumentParser(
        description='Generate RMarkdown reports from YAML configuration'
    )
    parser.add_argument(
        'config',
        help='YAML configuration file'
    )
    parser.add_argument(
        'template',
        nargs='?',
        default='template.rmd',
        help='RMarkdown template file (default: template.rmd)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output RMarkdown file path (if not specified, uses value from config.yml)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("   RMARKDOWN REPORT GENERATOR")
    print("="*60 + "\n")
    
    # 1. Load configuration
    config = load_config(args.config)
    
    # 2. Load template
    template = load_template(args.template)
    
    # 3. Render
    print("\nRendering template...")
    rendered_rmd = render_rmd(template, config)
    
    # 4. Determine output path
    output_path = args.output or config.get('output', {}).get('rmd_filename', 'report_generated.rmd')
    
    # 5. Save
    print("\nSaving file...")
    output_file = save_rmd(rendered_rmd, output_path)
    
    print("\n" + "="*60)
    print("✓ Report generated successfully!")
    print("="*60 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
