import os

import click
from sdrf_pipelines.sdrf.sdrf import read_sdrf


def parse_comment_value(value: str, key: str = "NT") -> str:
    """Parse a comment value in the format 'NT=value;AC=accession' and extract the specified key."""
    if not value or value.lower() in ["not available", "not applicable", "na", ""]:
        return ""

    if ";" not in value and "=" not in value:
        return value

    parts = value.split(";")
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            if k.strip().upper() == key.upper():
                return v.strip()
    return value


def get_sdrf_value(row, column_name: str, default: str = "") -> str:
    """Safely get a value from an SDRF row, returning default if column doesn't exist or value is not available."""
    try:
        value = row.get(column_name, default)
        if value is None or str(value).lower() in ["not available", "not applicable", "na"]:
            return default
        return str(value)
    except (KeyError, AttributeError):
        return default


def extract_unique_values(df, column_name: str) -> list:
    """Extract unique non-empty values from a DataFrame column."""
    try:
        values = df[column_name].unique()
        return [str(v) for v in values if v and str(v).lower() not in ["not available", "not applicable", "na", ""]]
    except KeyError:
        return []


@click.command()
@click.option("--sdrf_file", required=True, type=click.Path(exists=True), help="Path to the SDRF file.")
@click.option("--output_dir", required=True, type=click.Path(), help="Path to the output directory.")
@click.option("--asap_team_name", default="Alessi", help="ASAP team name.")
@click.option("--asap_lab_name", default="Dario Alessi", help="ASAP lab name.")
@click.option("--project_name", default="", help="Project name.")
@click.option("--project_description", default="", help="Project description.")
@click.option("--dataset_title", default="", help="Dataset title.")
@click.option("--dataset_description", default="", help="Dataset description.")
@click.option("--dataset_name", default="", help="Dataset name.")
@click.option("--pi_full_name", default="Dario R. Alessi", help="PI full name.")
@click.option("--pi_email", default="", help="PI email.")
@click.option("--contributor_names", default="", help="Contributor names.")
@click.option("--submitter_name", default="", help="Submitter name.")
@click.option("--submitter_email", default="", help="Submitter email.")
@click.option("--asap_grant_id", default="", help="ASAP grant ID.")
@click.option("--other_funding_source", default="", help="Other funding source.")
@click.option("--publication_doi", default="", help="Publication DOI.")
@click.option("--publication_pmid", default="", help="Publication PMID.")
@click.option("--number_samples", default="", help="Number of samples (auto-detected from SDRF if empty).")
@click.option("--sample_types", default="", help="Sample types (auto-detected from SDRF if empty).")
@click.option("--types_of_samples", default="", help="Types of samples (auto-detected from SDRF if empty).")
@click.option("--metadata_tables", default="SDRF.tsv", help="Metadata tables.")
@click.option("--dua_version", default="", help="DUA version.")
@click.option("--pi_orcid", default="", help="PI ORCID.")
@click.option("--pi_google_scholar_id", default="", help="PI Google Scholar ID.")
@click.option("--preprocessing_references", default="", help="Preprocessing references.")
@click.option("--metadata_version_date", default="", help="Metadata version date.")
@click.option("--alternate_dataset_id", default="", help="Alternate dataset ID.")
def main(
    sdrf_file: str,
    output_dir: str,
    asap_team_name: str,
    asap_lab_name: str,
    project_name: str,
    project_description: str,
    dataset_title: str,
    dataset_description: str,
    dataset_name: str,
    pi_full_name: str,
    pi_email: str,
    contributor_names: str,
    submitter_name: str,
    submitter_email: str,
    asap_grant_id: str,
    other_funding_source: str,
    publication_doi: str,
    publication_pmid: str,
    number_samples: str,
    sample_types: str,
    types_of_samples: str,
    metadata_tables: str,
    dua_version: str,
    pi_orcid: str,
    pi_google_scholar_id: str,
    preprocessing_references: str,
    metadata_version_date: str,
    alternate_dataset_id: str,
) -> None:
    """Export ASAP files from SDRF."""
    os.makedirs(output_dir, exist_ok=True)
    sdrf = read_sdrf(sdrf_file)
    df = sdrf.df

    auto_number_samples = str(df.shape[0])
    auto_sample_types = extract_unique_values(df, "characteristics[sample type]")
    auto_organisms = extract_unique_values(df, "characteristics[organism]")
    auto_tissues = extract_unique_values(df, "characteristics[organism part]")

    # DATA.csv
    data_file_header = ["sample_id", "replicate", "replicate_count", "repeated_sample", "batch", "file_type",
                        "file_name", "file_description", "file_MD5", "adjustment", "content", "header", "annotation",
                        "configuration_file"]
    result = [data_file_header]
    for n, r in df.iterrows():
        sample_id = ";".join((
            get_sdrf_value(r, "source name"),
            get_sdrf_value(r, "assay name"),
            get_sdrf_value(r, "comment[label]")
        ))
        replicate = get_sdrf_value(r, "characteristics[biological replicate]", "1")
        data_file = get_sdrf_value(r, "comment[data file]")
        acquisition_method = get_sdrf_value(r, "comment[proteomics data acquisition method]")

        data = [sample_id, replicate, "1", "0", "NA", "Raw", data_file, acquisition_method, "", "", "", "", ""]
        result.append(data)
    with open(os.path.join(output_dir, "DATA.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # CELL.csv
    cell_file_header = ["subject_id", "cell_line", "perturbation", "clone_level", "aux_table"]
    result = [cell_file_header]
    cell_lines = extract_unique_values(df, "characteristics[cell line]")
    if not cell_lines:
        line = ["NA", "NA", "NA", "NA", "NA"]
        result.append(line)
    else:
        for cell_line in cell_lines:
            line = [cell_line, cell_line, "NA", "NA", "NA"]
            result.append(line)
    with open(os.path.join(output_dir, "CELL.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # PROTEOMICS.csv
    proteomics_file_header = [
        "sample_id", "source_id", "subject_id", "sample_run", "technology", "protocol", "assay",
        "instrument", "technical_replicate", "raw_file", "summary_file", "SDRF_proteomics_table",
        "acquisition_method", "disease", "source", "search_engine", "database", "cleavage_agents",
        "modifications", "ms1_scan_range", "precursor_tolerance", "fragment_tolerance"
    ]
    result = [proteomics_file_header]
    for n, r in df.iterrows():
        sample_id = ";".join((
            get_sdrf_value(r, "source name"),
            get_sdrf_value(r, "assay name"),
            get_sdrf_value(r, "comment[label]")
        ))
        source_id = get_sdrf_value(r, "source name")
        replicate = get_sdrf_value(r, "characteristics[biological replicate]", "1")
        technology = get_sdrf_value(r, "technology type")
        sample_type = get_sdrf_value(r, "characteristics[sample type]")
        instrument_raw = get_sdrf_value(r, "comment[instrument]")
        instrument = parse_comment_value(instrument_raw, "NT")
        tech_replicate = get_sdrf_value(r, "comment[technical replicate]", "1")
        raw_file = get_sdrf_value(r, "comment[file uri]")
        acquisition_method = get_sdrf_value(r, "comment[proteomics data acquisition method]")
        disease = get_sdrf_value(r, "characteristics[disease]")
        search_engine = get_sdrf_value(r, "comment[search engine]")
        database = get_sdrf_value(r, "comment[database]")
        ms1_range = get_sdrf_value(r, "comment[ms1 scan range]")
        precursor_tol = get_sdrf_value(r, "comment[precursor mass tolerance]")
        fragment_tol = get_sdrf_value(r, "comment[fragment mass tolerance]")

        cleavage_agents = []
        for col in df.columns:
            if "cleavage agent details" in col.lower():
                agent = parse_comment_value(get_sdrf_value(r, col), "NT")
                if agent and agent not in cleavage_agents:
                    cleavage_agents.append(agent)
        cleavage_str = "; ".join(cleavage_agents)

        modifications = []
        for col in df.columns:
            if "modification parameters" in col.lower():
                mod_raw = get_sdrf_value(r, col)
                if mod_raw:
                    mod_name = parse_comment_value(mod_raw, "NT")
                    mod_type = parse_comment_value(mod_raw, "MT")
                    if mod_name:
                        mod_desc = f"{mod_name} ({mod_type})" if mod_type else mod_name
                        if mod_desc not in modifications:
                            modifications.append(mod_desc)
        mod_str = "; ".join(modifications)

        data = [
            sample_id, source_id, "", replicate, technology, "", sample_type,
            instrument, tech_replicate, raw_file, "NA", "SDRF.tsv",
            acquisition_method, disease, "NA", search_engine, database, cleavage_str,
            mod_str, ms1_range, precursor_tol, fragment_tol
        ]
        result.append(data)
    with open(os.path.join(output_dir, "PROTEOMICS.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # SAMPLE.csv
    sample_file_header = [
        "sample_id", "subject_id", "source_sample_id", "replicate", "replicate_count", "repeated_sample",
        "batch", "organism", "tissue", "assay_type", "condition_id", "organism_ontology_term_id",
        "age_at_collection", "time", "alternate_id", "development_stage_ontology_term_id",
        "sex_ontology_term_id", "self_reported_ethnicity_ontology_term_id", "disease_ontology_term_id",
        "tissue_ontology_term_id", "assay_ontology_term_id", "donor_id", "pm_PH", "cell_type_ontology_term_id",
        "source_RIN", "DV200", "suspension_type", "source_id", "enrichment_process", "strain", "cell_type"
    ]
    result = [sample_file_header]
    for n, r in df.iterrows():
        sample_id = ";".join((
            get_sdrf_value(r, "source name"),
            get_sdrf_value(r, "assay name"),
            get_sdrf_value(r, "comment[label]")
        ))
        source_name = get_sdrf_value(r, "source name")
        assay_name = get_sdrf_value(r, "assay name")
        replicate = get_sdrf_value(r, "characteristics[biological replicate]", "1")
        organism = get_sdrf_value(r, "characteristics[organism]")
        tissue = get_sdrf_value(r, "characteristics[organism part]")
        condition = get_sdrf_value(r, "characteristics[condition]")
        age = get_sdrf_value(r, "characteristics[age]")
        disease = get_sdrf_value(r, "characteristics[disease]")
        dev_stage = get_sdrf_value(r, "characteristics[developmental stage]")
        sex = get_sdrf_value(r, "characteristics[sex]")
        individual = get_sdrf_value(r, "characteristics[individual]")
        enrichment = get_sdrf_value(r, "characteristics[enrichment process]")
        strain = get_sdrf_value(r, "characteristics[strain/breed]")
        cell_type = get_sdrf_value(r, "characteristics[cell type]")

        data = [
            sample_id, individual, source_name, replicate, "1", "0", "NA",
            organism, tissue, "Proteomic", condition, "",
            age, "", assay_name, dev_stage,
            sex, "", disease, "", "", "", "", cell_type,
            "", "", "", source_name, enrichment, strain, cell_type
        ]
        result.append(data)
    with open(os.path.join(output_dir, "SAMPLE.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # STUDY.csv - auto-populate from SDRF if not provided via arguments
    final_number_samples = number_samples if number_samples else auto_number_samples
    final_sample_types = sample_types if sample_types else "; ".join(auto_sample_types)
    final_types_of_samples = types_of_samples if types_of_samples else "; ".join(auto_sample_types)

    auto_dataset_description_parts = []
    if auto_organisms:
        auto_dataset_description_parts.append(f"Organism: {', '.join(auto_organisms)}")
    if auto_tissues:
        auto_dataset_description_parts.append(f"Tissue: {', '.join(auto_tissues)}")
    if auto_sample_types:
        auto_dataset_description_parts.append(f"Sample type: {', '.join(auto_sample_types)}")
    auto_dataset_description = ". ".join(auto_dataset_description_parts)

    final_dataset_description = dataset_description if dataset_description else auto_dataset_description

    study_file_header = [
        "ASAP_team_name", "ASAP_lab_name", "project_name", "project_description", "dataset_title",
        "dataset_description", "dataset_name", "PI_full_name", "PI_email", "contributor_names",
        "submitter_name", "submitter_email", "ASAP_grant_id", "other_funding_source", "publication_DOI",
        "publication_PMID", "number_samples", "sample_types", "types_of_samples", "metadata_tables",
        "DUA_version", "PI_ORCID", "PI_google_scholar_id", "preprocessing_references",
        "metadata_version_date", "alternate_dataset_id"
    ]
    result = [study_file_header]
    line = [
        asap_team_name, asap_lab_name, project_name, project_description, dataset_title,
        final_dataset_description, dataset_name, pi_full_name, pi_email, contributor_names,
        submitter_name, submitter_email, asap_grant_id, other_funding_source,
        publication_doi, publication_pmid, final_number_samples, final_sample_types,
        final_types_of_samples, metadata_tables, dua_version, pi_orcid,
        pi_google_scholar_id, preprocessing_references, metadata_version_date,
        alternate_dataset_id
    ]
    result.append(line)
    with open(os.path.join(output_dir, "STUDY.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # intervention.csv - group samples by condition and collect subject_ids
    unique_conditions = extract_unique_values(df, "characteristics[condition]")
    if not unique_conditions:
        unique_conditions = extract_unique_values(df, "factor value[condition]")

    condition_subjects = {}
    condition_sample_types = {}
    for n, r in df.iterrows():
        condition = get_sdrf_value(r, "characteristics[condition]")
        if not condition:
            condition = get_sdrf_value(r, "factor value[condition]")
        if condition:
            if condition not in condition_subjects:
                condition_subjects[condition] = []
                condition_sample_types[condition] = set()
            source = get_sdrf_value(r, "source name")
            if source and source not in condition_subjects[condition]:
                condition_subjects[condition].append(source)
            sample_type = get_sdrf_value(r, "characteristics[sample type]")
            if sample_type:
                condition_sample_types[condition].add(sample_type)

    intervention_file_header = ["condition_id", "intervention_id", "intervention_description", "subject_ids"]
    result = [intervention_file_header]
    for condition in unique_conditions:
        subjects = ", ".join(condition_subjects.get(condition, []))
        sample_types_str = ", ".join(condition_sample_types.get(condition, []))
        description = f"Condition: {condition}"
        if sample_types_str:
            description += f". Sample type: {sample_types_str}"
        data = [condition, condition, description, subjects]
        result.append(data)
    with open(os.path.join(output_dir, "intervention.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # CONDITION.csv
    condition_file_header = ["condition_id", "intervention_name", "intervention_id", "protocol_id", "intervention_aux_table"]
    result = [condition_file_header]
    for condition in unique_conditions:
        data = [condition, condition, condition, "NA", "intervention.csv"]
        result.append(data)
    with open(os.path.join(output_dir, "CONDITION.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")

    # PROTOCOL.csv - Template with headers only (requires manual input)
    protocol_file_header = [
        "sample_collection_summary", "cell_extraction_summary", "lib_prep_summary",
        "data_processing_summary", "github_url", "protocols_io_DOI", "other_reference"
    ]
    result = [protocol_file_header]
    result.append(["", "", "", "", "", "", ""])
    with open(os.path.join(output_dir, "PROTOCOL.csv"), "w") as f:
        for row in result:
            f.write(",".join(str(x) for x in row) + "\n")


if __name__ == "__main__":
    main()