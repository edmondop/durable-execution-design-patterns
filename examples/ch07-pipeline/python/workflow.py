from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow


@dataclass
class PipelineInput:
    source_path: str
    destination_table: str


@dataclass
class ParseResult:
    record_count: int
    raw_records: list[dict]


@dataclass
class ValidatedData:
    valid_records: list[dict]
    rejected_count: int


@dataclass
class EnrichedData:
    records: list[dict]


@activity.defn
async def parse_csv(source_path: str) -> ParseResult:
    print(f"Parsing {source_path}")
    return ParseResult(record_count=1000, raw_records=[{"id": i} for i in range(1000)])


@activity.defn
async def validate_schema(data: ParseResult) -> ValidatedData:
    print(f"Validating {data.record_count} records")
    return ValidatedData(valid_records=data.raw_records, rejected_count=0)


@activity.defn
async def enrich_records(data: ValidatedData) -> EnrichedData:
    print(f"Enriching {len(data.valid_records)} records")
    return EnrichedData(records=[{**r, "enriched": True} for r in data.valid_records])


@activity.defn
async def load_to_warehouse(data: EnrichedData, table: str) -> int:
    print(f"Loading {len(data.records)} records to {table}")
    return len(data.records)


# tag::pipeline[]
@workflow.defn
class ETLPipelineWorkflow:
    @workflow.run
    async def run(self, input: PipelineInput) -> str:
        # Stage 1: Parse — checkpoint after completion
        parsed = await workflow.execute_activity(
            parse_csv,
            input.source_path,
            start_to_close_timeout=timedelta(minutes=10),
        )

        # Stage 2: Validate — crash here, replay skips Stage 1
        validated = await workflow.execute_activity(
            validate_schema,
            parsed,
            start_to_close_timeout=timedelta(minutes=5),
        )

        # Stage 3: Enrich — the expensive stage
        enriched = await workflow.execute_activity(
            enrich_records,
            validated,
            start_to_close_timeout=timedelta(hours=2),
        )

        # Stage 4: Load — final stage
        loaded_count = await workflow.execute_activity(
            load_to_warehouse,
            args=[enriched, input.destination_table],
            start_to_close_timeout=timedelta(minutes=30),
        )

        return f"Pipeline complete: {loaded_count} records loaded to {input.destination_table}"
# end::pipeline[]
