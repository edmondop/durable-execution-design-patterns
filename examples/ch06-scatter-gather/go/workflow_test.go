package scattergather

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.temporal.io/sdk/testsuite"
)

func TestPriceComparison_ReturnsResultsFromAllAirlines(t *testing.T) {
	testSuite := &testsuite.WorkflowTestSuite{}
	env := testSuite.NewTestWorkflowEnvironment()

	env.RegisterWorkflow(PriceComparisonWorkflow)
	env.RegisterActivity(SearchAirline)

	req := PriceRequest{
		SearchID: "search-1",
		Origin:   "SFO",
		Dest:     "JFK",
		Date:     "2025-06-15",
	}

	env.ExecuteWorkflow(PriceComparisonWorkflow, req)

	require.True(t, env.IsWorkflowCompleted())
	require.NoError(t, env.GetWorkflowError())

	var results []PriceResult
	require.NoError(t, env.GetWorkflowResult(&results))

	assert.Len(t, results, 5)
	for _, r := range results {
		assert.NotEmpty(t, r.Airline)
		assert.Greater(t, r.Price, 0.0)
		assert.Empty(t, r.Err)
	}
}
