from sdrf_pipelines.sdrf.sdrf import SDRFDataFrame, read_sdrf
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Export ASAP files from SDRF.")
    parser.add_argument("--sdrf_file", required=True, help="Path to the SDRF file.")
    parser.add_argument("--output_dir", required=True, help="Path to the output directory.")

    # Arguments for STUDY.csv
    parser.add_argument("--asap_team_name", default="Alessi", help="ASAP team name")
    parser.add_argument("--asap_lab_name", default="Dario Alessi", help="ASAP lab name")
    parser.add_argument("--project_name", default="", help="Project name")
    parser.add_argument("--project_description", default="", help="Project description")
    parser.add_argument("--dataset_title", default="", help="Dataset title")
    parser.add_argument("--dataset_description", default="", help="Dataset description")
    parser.add_argument("--dataset_name", default="", help="Dataset name")
    parser.add_argument("--pi_full_name", default="Dario R. Alessi", help="PI full name")
    parser.add_argument("--pi_email", default="", help="PI email")
    parser.add_argument("--contributor_names", default="", help="Contributor names")
    parser.add_argument("--submitter_name", default="", help="Submitter name")
    parser.add_argument("--submitter_email", default="", help="Submitter email")
    parser.add_argument("--asap_grant_id", default="", help="ASAP grant ID")
    parser.add_argument("--other_funding_source", default="", help="Other funding source")
    parser.add_argument("--publication_doi", default="", help="Publication DOI")
    parser.add_argument("--publication_pmid", default="", help="Publication PMID")
    parser.add_argument("--number_samples", default="", help="Number of samples")
    parser.add_argument("--sample_types", default="", help="Sample types")
    parser.add_argument("--types_of_samples", default="", help="Types of samples")
    parser.add_argument("--metadata_tables", default="SDRF.tsv", help="Metadata tables")
    parser.add_argument("--dua_version", default="", help="DUA version")
    parser.add_argument("--pi_orcid", default="", help="PI ORCID")
    parser.add_argument("--pi_google_scholar_id", default="", help="PI Google Scholar ID")
    parser.add_argument("--preprocessing_references", default="", help="Preprocessing references")
    parser.add_argument("--metadata_version_date", default="", help="Metadata version date")
    parser.add_argument("--alternate_dataset_id", default="", help="Alternate dataset ID")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    df = read_sdrf(args.sdrf_file)

    # DATA.csv
    data_file_header = ["sample_id", "replicate", "replicate_count", "repeated_sample", "batch", "file_type",
                        "file_name", "file_description", "file_MD5", "adjustment", "content", "header", "annotation",
                        "configuration_file"]
    result = [data_file_header]
    for n, r in df.iterrows():
        data = [";".join((r["source name"], r["assay name"], r["comment[label]"],)),
                r["characteristics[biological replicate]"], "1", "0", "NA", "Raw", r["comment[data file]"],
                r["comment[proteomics data acquisition method]"], "", "", "", "", ""]
        result.append(data)
    with open(os.path.join(args.output_dir, "DATA.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")

    # CELL.csv
    cell_file_header = ["subject_id", "cell_line", "perturbation", "clone_level", "aux_table"]
    result = [cell_file_header]
    cell_lines = df["characteristics[cell line]"].unique()
    if len(cell_lines) == 1 and cell_lines[0].lower() in ["not applicable", "not available"]:
        line = ["NA", "NA", "NA", "NA", "NA"]
        result.append(line)
    else:
        for cell_line in cell_lines:
            line = [cell_line, cell_line, "NA", "NA", "NA"]
            result.append(line)
    with open(os.path.join(args.output_dir, "CELL.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")

    # PROTEOMICS.csv
    proteomics_file_header = ["sample_id", "source_id", "subject_id", "sample_run", "technology", "protocol", "assay",
                               "instrument", "technical_replicate", "raw_file", "summary_file",
                               "SDRF_proteomics_table", "protocol", "disease", "source"]
    result = [proteomics_file_header]
    for n, r in df.iterrows():
        data = [";".join((r["source name"], r["assay name"], r["comment[label]"],)), r["source name"], "",
                r["characteristics[biological replicate]"], r["technology type"], "", r["characteristics[sample type]"],
                r["comment[instrument]"], r["comment[technical replicate]"], r["comment[file uri]"], "NA", "SDRF.tsv",
                "", r["characteristics[disease]"], "NA"]
        result.append(data)
    with open(os.path.join(args.output_dir, "PROTEOMICS.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")

    # SAMPLE.csv
    sample_file_header = "sample_id\tsubject_id\tsource_sample_id\treplicate\treplicate_count\trepeated_sample\tbatch\torganism\ttissue\tassay_type\tcondition_id\torganism_ontology_term_id\tage_at_collection\ttime\talternate_id\tdevelopment_stage_ontology_term_id\tsex_ontology_term_id\tself_reported_ethnicity_ontology_term_id\tdisease_ontology_term_id\ttissue_ontology_term_id\tassay_ontology_term_id\tdonor_id\tpm_PH\tcell_type_ontology_term_id\tsource_RIN\tDV200\tsuspension_type\tsource_id".split(
        "\t")
    result = [sample_file_header]
    for n, r in df.iterrows():
        data = [";".join((r["source name"], r["assay name"], r["comment[label]"],)), "", "", "1", "1", "0", "NA",
                r["characteristics[organism]"], r["characteristics[organism part]"], "Proteomic",
                r["characteristics[condition]"], "", r.get("characteristics[age]", "not available"), "",
                r["assay name"], "", "", r.get("characteristics[disease]", ""), "", "", "", "", "", "", "", "",
                r["source name"]]
        result.append(data)
    with open(os.path.join(args.output_dir, "SAMPLE.csv"), "w") as f:
        for row in result:
            f.write(",".join(map(str, row)) + "\n")

    # STUDY.csv
    study_file_header = "ASAP_team_name\tASAP_lab_name\tproject_name\tproject_description\tdataset_title\tdataset_description\tdataset_name\tPI_full_name\tPI_email\tcontributor_names\tsubmitter_name\tsubmitter_email\tASAP_grant_id\tother_funding_source\tpublication_DOI\tpublication_PMID\tnumber_samples\tsample_types\ttypes_of_samples\tmetadata_tables\tDUA_version\tPI_ORCID\tPI_google_scholar_id\tpreprocessing_references\tmetadata_version_date\talternate_dataset_id".split(
        "\t")
    result = [study_file_header]
    line = [args.asap_team_name, args.asap_lab_name, args.project_name, args.project_description, args.dataset_title,
            args.dataset_description, args.dataset_name, args.pi_full_name, args.pi_email, args.contributor_names,
            args.submitter_name, args.submitter_email, args.asap_grant_id, args.other_funding_source,
            args.publication_doi, args.publication_pmid, args.number_samples, args.sample_types,
            args.types_of_samples, args.metadata_tables, args.dua_version, args.pi_orcid,
            args.pi_google_scholar_id, args.preprocessing_references, args.metadata_version_date,
            args.alternate_dataset_id]
    result.append(line)
    with open(os.path.join(args.output_dir, "STUDY.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")

    # intervention.csv
    unique_conditions = df["characteristics[condition]"].unique()
    intervention_file_header = "condition_id\tintervention_id\tintervention_description\tsubject_ids".split("\t")
    result = [intervention_file_header]
    added_conditions = set()
    for n, r in df.iterrows():
        if r.get("characteristics[condition]", "") in added_conditions:
            continue
        data = [r.get("characteristics[condition]", ""), "", "", ""]
        result.append(data)
        added_conditions.add(r.get("characteristics[condition]", ""))
    with open(os.path.join(args.output_dir, "intervention.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")

    # CONDITION.csv
    condition_file_header = "condition_id\tintervention_name\tintervention_id\tprotocol_id\tintervention_aux_table".split(
        "\t")
    result = [condition_file_header]
    for condition in unique_conditions:
        data = [condition, "", "", "NA", "intervention.csv"]
        result.append(data)
    with open(os.path.join(args.output_dir, "CONDITION.csv"), "w") as f:
        for row in result:
            f.write(",".join(row) + "\n")


if __name__ == "__main__":
    main()