# Export ASAP


## Installation

<a href="cauldron://install?repo=https%3A%2F%2Fgithub.com%2Fnoatgnu%2Fexport_asap_plugin">⬇️ <strong>Click here to install in Cauldron</strong></a>

> **Repository**: `https://github.com/noatgnu/export_asap_plugin`

**Manual installation:**

1. Open Cauldron
2. Go to **Plugins** → **Install from Repository**
3. Paste: `https://github.com/noatgnu/export_asap_plugin`
4. Click **Install**

**ID**: `export-asap`  
**Version**: 1.0.0  
**Category**: utilities  
**Author**: 

## Description

Exports ASAP files from an SDRF file.

## Runtime

- **Type**: `python`
- **Script**: `export_asap.py`

## Inputs

| Name | Label | Type | Required | Default | Visibility |
|------|-------|------|----------|---------|------------|
| `sdrf_file` | SDRF File | file | Yes | - | Always visible |
| `asap_team_name` | ASAP Team Name | text | No | Alessi | Always visible |
| `asap_lab_name` | ASAP Lab Name | text | No | Dario Alessi | Always visible |
| `pi_full_name` | PI Full Name | text | No | Dario R. Alessi | Always visible |
| `project_name` | Project Name | text | No |  | Always visible |
| `project_description` | Project Description | text | No |  | Always visible |
| `dataset_title` | Dataset Title | text | No |  | Always visible |
| `dataset_description` | Dataset Description | text | No |  | Always visible |
| `dataset_name` | Dataset Name | text | No |  | Always visible |
| `pi_email` | PI Email | text | No |  | Always visible |
| `contributor_names` | Contributor Names | text | No |  | Always visible |
| `submitter_name` | Submitter Name | text | No |  | Always visible |
| `submitter_email` | Submitter Email | text | No |  | Always visible |
| `asap_grant_id` | ASAP Grant ID | text | No |  | Always visible |
| `other_funding_source` | Other Funding Source | text | No |  | Always visible |
| `publication_doi` | Publication DOI | text | No |  | Always visible |
| `publication_pmid` | Publication PMID | text | No |  | Always visible |
| `number_samples` | Number of Samples | text | No |  | Always visible |
| `sample_types` | Sample Types | text | No |  | Always visible |
| `types_of_samples` | Types of Samples | text | No |  | Always visible |
| `metadata_tables` | Metadata Tables | text | No | SDRF.tsv | Always visible |
| `dua_version` | DUA Version | text | No |  | Always visible |
| `pi_orcid` | PI ORCID | text | No |  | Always visible |
| `pi_google_scholar_id` | PI Google Scholar ID | text | No |  | Always visible |
| `preprocessing_references` | Preprocessing References | text | No |  | Always visible |
| `metadata_version_date` | Metadata Version Date | text | No |  | Always visible |
| `alternate_dataset_id` | Alternate Dataset ID | text | No |  | Always visible |

### Input Details

#### SDRF File (`sdrf_file`)

The input SDRF file in .tsv format.


#### ASAP Team Name (`asap_team_name`)

Name of the ASAP team.


#### ASAP Lab Name (`asap_lab_name`)

Name of the ASAP lab.


#### PI Full Name (`pi_full_name`)

Full name of the Principal Investigator.


#### Project Name (`project_name`)


#### Project Description (`project_description`)


#### Dataset Title (`dataset_title`)


#### Dataset Description (`dataset_description`)


#### Dataset Name (`dataset_name`)


#### PI Email (`pi_email`)


#### Contributor Names (`contributor_names`)


#### Submitter Name (`submitter_name`)


#### Submitter Email (`submitter_email`)


#### ASAP Grant ID (`asap_grant_id`)


#### Other Funding Source (`other_funding_source`)


#### Publication DOI (`publication_doi`)


#### Publication PMID (`publication_pmid`)


#### Number of Samples (`number_samples`)


#### Sample Types (`sample_types`)


#### Types of Samples (`types_of_samples`)


#### Metadata Tables (`metadata_tables`)


#### DUA Version (`dua_version`)


#### PI ORCID (`pi_orcid`)


#### PI Google Scholar ID (`pi_google_scholar_id`)


#### Preprocessing References (`preprocessing_references`)


#### Metadata Version Date (`metadata_version_date`)


#### Alternate Dataset ID (`alternate_dataset_id`)


## Outputs

| Name | File | Type | Format | Description |
|------|------|------|--------|-------------|
| `output_dir` | `.` |  |  |  |

## Requirements

- **Python**: >=3.8
- **Additional Packages**:
  - sdrf_pipelines
  - pandas

## Usage

### Via UI

1. Navigate to **utilities** → **Export ASAP**
2. Fill in the required inputs
3. Click **Run Analysis**

### Via Plugin System

```typescript
const jobId = await pluginService.executePlugin('export-asap', {
  // Add parameters here
});
```
