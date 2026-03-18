package scattergather

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/workflow"
)

type PriceRequest struct {
	SearchID string
	Origin   string
	Dest     string
	Date     string
}

type PriceResult struct {
	Airline string
	Price   float64
	Err     string
}

// tag::scatter_gather[]
func PriceComparisonWorkflow(ctx workflow.Context, req PriceRequest) ([]PriceResult, error) {
	airlines := []string{"united", "delta", "american", "southwest", "jetblue"}

	// Scatter: launch all searches in parallel
	var futures []workflow.Future
	for _, airline := range airlines {
		actCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
			StartToCloseTimeout: 10 * time.Second,
		})
		f := workflow.ExecuteActivity(actCtx, SearchAirline, airline, req)
		futures = append(futures, f)
	}

	// Gather: collect results with a deadline
	var results []PriceResult
	deadline := workflow.NewTimer(ctx, 8*time.Second)

	for _, f := range futures {
		selector := workflow.NewSelector(ctx)

		var deadlineHit bool
		selector.AddFuture(f, func(f workflow.Future) {
			var result PriceResult
			if err := f.Get(ctx, &result); err != nil {
				result = PriceResult{Err: err.Error()}
			}
			results = append(results, result)
		})

		selector.AddFuture(deadline, func(f workflow.Future) {
			// Deadline hit — return what we have
			deadlineHit = true
		})

		selector.Select(ctx)
		if deadlineHit {
			break
		}
	}

	if len(results) == 0 {
		return nil, fmt.Errorf("no results within deadline for search %s", req.SearchID)
	}

	return results, nil
}

// end::scatter_gather[]
