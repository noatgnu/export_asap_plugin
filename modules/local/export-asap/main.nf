process EXPORT_ASAP {
    label 'process_medium'

    container "${ workflow.containerEngine == 'singularity' ?
        'docker://cauldron/export-asap:1.0.0' :
        'cauldron/export-asap:1.0.0' }"

    input:
    path sdrf_file
    val asap_team_name
    val asap_lab_name
    val pi_full_name
    val project_name
    val project_description
    val dataset_title
    val dataset_description
    val dataset_name
    val pi_email
    val contributor_names
    val submitter_name
    val submitter_email
    val asap_grant_id
    val other_funding_source
    val publication_doi
    val publication_pmid
    val number_samples
    val sample_types
    val types_of_samples
    val metadata_tables
    val dua_version
    val pi_orcid
    val pi_google_scholar_id
    val preprocessing_references
    val metadata_version_date
    val alternate_dataset_id

    output:
    
    path ".", emit: output_dir, optional: true
    path "versions.yml", emit: versions

    script:
    def args = task.ext.args ?: ''
    """
    # Build arguments dynamically to match CauldronGO PluginExecutor logic
    ARG_LIST=()

    
    # Mapping for dataset_name
    VAL="$dataset_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--dataset_name" "\$VAL")
    fi
    
    # Mapping for submitter_email
    VAL="$submitter_email"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--submitter_email" "\$VAL")
    fi
    
    # Mapping for asap_grant_id
    VAL="$asap_grant_id"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--asap_grant_id" "\$VAL")
    fi
    
    # Mapping for publication_doi
    VAL="$publication_doi"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--publication_doi" "\$VAL")
    fi
    
    # Mapping for preprocessing_references
    VAL="$preprocessing_references"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--preprocessing_references" "\$VAL")
    fi
    
    # Mapping for metadata_version_date
    VAL="$metadata_version_date"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--metadata_version_date" "\$VAL")
    fi
    
    # Mapping for sdrf_file
    VAL="$sdrf_file"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--sdrf_file" "\$VAL")
    fi
    
    # Mapping for asap_team_name
    VAL="$asap_team_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--asap_team_name" "\$VAL")
    fi
    
    # Mapping for pi_full_name
    VAL="$pi_full_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--pi_full_name" "\$VAL")
    fi
    
    # Mapping for dataset_description
    VAL="$dataset_description"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--dataset_description" "\$VAL")
    fi
    
    # Mapping for pi_email
    VAL="$pi_email"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--pi_email" "\$VAL")
    fi
    
    # Mapping for other_funding_source
    VAL="$other_funding_source"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--other_funding_source" "\$VAL")
    fi
    
    # Mapping for publication_pmid
    VAL="$publication_pmid"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--publication_pmid" "\$VAL")
    fi
    
    # Mapping for alternate_dataset_id
    VAL="$alternate_dataset_id"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--alternate_dataset_id" "\$VAL")
    fi
    
    # Mapping for project_name
    VAL="$project_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--project_name" "\$VAL")
    fi
    
    # Mapping for contributor_names
    VAL="$contributor_names"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--contributor_names" "\$VAL")
    fi
    
    # Mapping for submitter_name
    VAL="$submitter_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--submitter_name" "\$VAL")
    fi
    
    # Mapping for sample_types
    VAL="$sample_types"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--sample_types" "\$VAL")
    fi
    
    # Mapping for pi_google_scholar_id
    VAL="$pi_google_scholar_id"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--pi_google_scholar_id" "\$VAL")
    fi
    
    # Mapping for asap_lab_name
    VAL="$asap_lab_name"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--asap_lab_name" "\$VAL")
    fi
    
    # Mapping for dataset_title
    VAL="$dataset_title"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--dataset_title" "\$VAL")
    fi
    
    # Mapping for number_samples
    VAL="$number_samples"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--number_samples" "\$VAL")
    fi
    
    # Mapping for types_of_samples
    VAL="$types_of_samples"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--types_of_samples" "\$VAL")
    fi
    
    # Mapping for metadata_tables
    VAL="$metadata_tables"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--metadata_tables" "\$VAL")
    fi
    
    # Mapping for dua_version
    VAL="$dua_version"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--dua_version" "\$VAL")
    fi
    
    # Mapping for pi_orcid
    VAL="$pi_orcid"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--pi_orcid" "\$VAL")
    fi
    
    # Mapping for project_description
    VAL="$project_description"
    if [ -n "\$VAL" ] && [ "\$VAL" != "null" ] && [ "\$VAL" != "[]" ]; then
        ARG_LIST+=("--project_description" "\$VAL")
    fi
    
    python /app/export_asap.py \
        "\${ARG_LIST[@]}" \
        --output_dir . \
        \${args:-}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        Export ASAP: 1.0.0
    END_VERSIONS
    """
}
