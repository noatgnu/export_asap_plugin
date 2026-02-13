#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { EXPORT_ASAP } from './modules/local/export-asap/main'

workflow PIPELINE {
    main:
    EXPORT_ASAP (
        params.sdrf_file ? Channel.fromPath(params.sdrf_file).collect() : Channel.of([]),
        Channel.value(params.asap_team_name ?: ''),
        Channel.value(params.asap_lab_name ?: ''),
        Channel.value(params.pi_full_name ?: ''),
        Channel.value(params.project_name ?: ''),
        Channel.value(params.project_description ?: ''),
        Channel.value(params.dataset_title ?: ''),
        Channel.value(params.dataset_description ?: ''),
        Channel.value(params.dataset_name ?: ''),
        Channel.value(params.pi_email ?: ''),
        Channel.value(params.contributor_names ?: ''),
        Channel.value(params.submitter_name ?: ''),
        Channel.value(params.submitter_email ?: ''),
        Channel.value(params.asap_grant_id ?: ''),
        Channel.value(params.other_funding_source ?: ''),
        Channel.value(params.publication_doi ?: ''),
        Channel.value(params.publication_pmid ?: ''),
        Channel.value(params.number_samples ?: ''),
        Channel.value(params.sample_types ?: ''),
        Channel.value(params.types_of_samples ?: ''),
        Channel.value(params.metadata_tables ?: ''),
        Channel.value(params.dua_version ?: ''),
        Channel.value(params.pi_orcid ?: ''),
        Channel.value(params.pi_google_scholar_id ?: ''),
        Channel.value(params.preprocessing_references ?: ''),
        Channel.value(params.metadata_version_date ?: ''),
        Channel.value(params.alternate_dataset_id ?: ''),
    )
}

workflow {
    PIPELINE ()
}
