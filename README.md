# TemplateShotgunMetagenomics
Here you can find all the scripts to run the whole shotgun metagenomics pipelines from the fastqs until the post-analysis.
This is project is still ongoing so you can find here a Beta Version.

This system allows generating customized RMarkdown reports from a YAML configuration file. The analyses (alpha diversity, beta diversity, PERMANOVA, etc.) are automatically generated according to the feature columns specified in the configuration.

## Files Included

### 1. `config.yml`
YAML configuration file containing all the necessary information:

- **Metadata**: Title, author, date
- **Project Information**: IP, Researcher, technology, species, samples
- **Background and sample description**: Free text
- **Input files**: Paths to phyloseq file and output directory
- **Feature columns**: Which metadata variables to analyze
- **Filtering parameters**: Relative abundance and prevalence cutoff
- **Analyses to perform**: Alpha diversity, beta diversity, ordination, PERMANOVA, DAA
- **Normalizations**: Parameters for transformations (CLR, pseudocounts, etc.)

### 2. `generate_rmd.py`

Python script that generates the final RMarkdown. It performs:

1. Reading the config.yml file
2. Reading the template.rmd template
3. Rendering with Jinja2 using the config values
4. Saving the generated RMarkdown file

### 3. `template.rmd`
RMarkdown template written in R+Jinja2 that defines the report structure:

- Sections: Introduction, Project Info, Background, Samples
- Dynamically generated analyses according to feature_columns!! Very Important to adapt config.yml to the features of the metadata!!
- Jinja2 loops that create sections for each metadata variable
- R chunks for alpha diversity, beta diversity, PERMANOVA, etc.
- New additions are easy to do

## Requisites

### R (in RMarkdown)
Los siguientes paquetes deben estar instalados:
- phyloseq
- vegan
- ggplot2
- dplyr
- microbiome
- BiocStyle
- patchwork
- ggrepel
- stringr
- tidyr
- viridis
- ggpubr
- knitr
- kableExtra
- DT
- umap
- readxl
- readr
- RVAideMemoire
- uwot
- BasicPlots

## Usage

### Step 1: Edit the configuration file

Open `config.yml` and customize::

```yaml
# Metadata
metadata:
  title: "Your title"
  author: "Your name"
  date: "auto"  # Or specify a date

# Project information
project_info:
  pi: "PI Name"
  researcher: "Researcher name"
  # ... etc

# Metadata source from XLSX
metadata_source:
  excel_file: "/path/to/your/metadata.xlsx"
  metadata_sheet: "metadata"
  sample_id_column: "Sample"

# Columns you want to analyze
feature_columns:
  - "Timepoint"
  - "pCR"
  - "Site"
  - "OtherVariable"

# Files
input_files:
  phyloseq_object: "/path/to/your/phyloseq.rds"
  output_directory: "/path/where/to/save/plots"
```

**Important!**: Focus on editing:
- `feature_columns`: The columns from your metadata file you want to analyze
- `input_files.phyloseq_object`: The path to your phyloseq object

### Step 2: Run the generator

From the command line in the folder containing the files:

```bash
# Basic form (automatically looks for template.rmd)
python generate_rmd.py config.yml

# Or specify manually
python generate_rmd.py config.yml template.rmd

# Or specify custom output path
python generate_rmd.py config.yml template.rmd -o /custom/path/report.rmd
```

### Step 3: Render the RMarkdown

## Ejemplo de flujo completo

```bash
# 1. Edit configuration
nano config.yml

# 2. Generate RMarkdown
python generate_rmd.py config.yml

# 3. Render to HTML
Rscript -e "rmarkdown::render('20260421_PNuciforo_PORTRAIT_SM_downstream_generated.rmd')"
```

## How the template works

The RMarkdown template uses Jinja2 to dynamically generate analyses:

### Bucles sobre feature_columns

```jinja2
{% for feature in feature_columns %}

# Analysis by: {{ feature }} {.tabset}

## Alpha Diversity - {{ feature }}
## Beta Diversity - {{ feature }}
## PERMANOVA - {{ feature }}

{% endfor %}
```

For each column in  `feature_columns`, the following are **automatically** generated:

1. **Alpha Diversity**:
   - Shannon Index
   - Chao1 Index

2. **Beta Diversity**:
   - PCOA
   - PCA
   - UMAP

3. **PERMANOVA** (if enabled):
   - PERMANOVA test

## Variables de configuración disponibles

Dentro del template, tienes acceso a:

- `{{ metadata.title }}` - Report title
- `{{ metadata.author }}` - Author
- `{{ metadata.date_rendered }}` - Date
- `{{ project_info.pi }}` - IP
- `{{ analyses.alpha_diversity | join(', ') }}` - Alpha diversity methods
- `{{ analyses.beta_diversity | join(', ') }}` - Beta diversity methods
- `{{ filtering.rel_abundance }}` - Relative abundance threshold
- etc...

## Advanced customization

### Modify the template

You can edit  `template.rmd` to:
- Add new sections
- Change the analysis order
- Adjust plot parameters
- Add custom analyses

Example: Add a new alpha diversity metric

```jinja2
### Simpson Index

```{r simpson_{{ loop.index0 }}}
simpson_df <- data.frame(
  Sample = sample_names(physeq_filtered),
  Simpson = diversity(t(physeq_filtered@otu_table), index = "simpson")
)

```
```

### Modify the configuration

You can have multiple `config.yml`:

```bash
python generate_rmd.py config_baseline.yml
python generate_rmd.py config_followup.yml
python generate_rmd.py config_species_level.yml
```

## Troubleshooting

### YAML parsing error

Check YAML syntax (spaces, indentation). 

### Template does not render correctly

Verify that:
- The paths in `config.yml` are correct
- The columns in `feature_columns` exist in your phyloseq
- The necessary R packages are installed


## Contacto

Para dudas o mejoras, revisa los comentarios en los archivos o adapta según tus necesidades específicas.
