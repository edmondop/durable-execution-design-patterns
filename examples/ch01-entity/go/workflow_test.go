package entity

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.temporal.io/sdk/testsuite"
)

func TestCartWorkflow_AddItem_UpdatesState(t *testing.T) {
	testSuite := &testsuite.WorkflowTestSuite{}
	env := testSuite.NewTestWorkflowEnvironment()

	env.RegisterWorkflow(CartWorkflow)

	// Add an item via signal
	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("addItem", AddItemCommand{
			Item: CartItem{
				ProductID: "prod-1",
				Name:      "Mechanical Keyboard",
				Price:     149.99,
				Quantity:  1,
			},
		})
	}, 0)

	// Then checkout to terminate
	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("checkout", struct{}{})
	}, 0)

	env.ExecuteWorkflow(CartWorkflow, "cart-123")

	assert.True(t, env.IsWorkflowCompleted())
}

func TestCartWorkflow_ReturnsStateWithItems(t *testing.T) {
	testSuite := &testsuite.WorkflowTestSuite{}
	env := testSuite.NewTestWorkflowEnvironment()

	env.RegisterWorkflow(CartWorkflow)

	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("addItem", AddItemCommand{
			Item: CartItem{
				ProductID: "prod-1",
				Name:      "Mechanical Keyboard",
				Price:     149.99,
				Quantity:  1,
			},
		})
	}, 0)

	env.RegisterDelayedCallback(func() {
		env.SignalWorkflow("checkout", struct{}{})
	}, 0)

	env.ExecuteWorkflow(CartWorkflow, "cart-123")

	require.True(t, env.IsWorkflowCompleted())
	require.NoError(t, env.GetWorkflowError())

	var state CartState
	require.NoError(t, env.GetWorkflowResult(&state))
	assert.Equal(t, "cart-123", state.ID)
	assert.Len(t, state.Items, 1)
	assert.Equal(t, "Mechanical Keyboard", state.Items[0].Name)
	assert.Equal(t, 149.99, state.Total())
}
