# Variants and Lineage

## Purpose
Track metric variants and their lineage.
Allow safe evolution without breaking consumers.

## Variant model
- parent_metric_id
- variant_metric_id
- reason and notes
- effective window
- release_channel
- owners

## Lineage
Record inputs for each metric.
Record upstream GDP contracts and transforms.
Record release and deprecation history.

## Release channels
Use dev, test, and prod channels.
Allow side by side variants during change windows.
