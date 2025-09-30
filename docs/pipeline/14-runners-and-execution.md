# Runners and Execution

## Purpose
Select the right compute runner for each workload.
Describe how the platform starts, monitors, and finishes jobs.

## Runners on AWS
- AWS Lambda
- AWS Glue
- Amazon ECS Fargate
- Amazon EMR
- AWS Batch
- AWS Step Functions for workflow control
- Amazon MWAA for Airflow
- Amazon AppFlow for SaaS pulls and pushes

## Selection guide
Use Lambda for light extracts that are short and bursty.
Use Glue for scheduled ETL jobs that use Spark or SQL.
Use Fargate for custom containers.
Use EMR for large Spark transforms.
Use Batch for heavy compute jobs.
Use Step Functions when you need workflow state.
Use MWAA for Airflow native DAGs.
Use AppFlow for managed SaaS transfers.

## Execution model
Jobs are stateless.
State is stored in evidence, lineage, and checkpoint stores.
Jobs receive a run configuration and a contract list.
Jobs emit logs, metrics, and evidence.
