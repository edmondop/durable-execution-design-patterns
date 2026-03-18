package entity

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/workflow"
)

type CartItem struct {
	ProductID string
	Name      string
	Price     float64
	Quantity  int
}

type CartState struct {
	ID        string
	Items     []CartItem
	Coupon    string
	UpdatedAt time.Time
}

func (s *CartState) Total() float64 {
	var total float64
	for _, item := range s.Items {
		total += item.Price * float64(item.Quantity)
	}
	return total
}

type AddItemCommand struct {
	Item CartItem
}

type RemoveItemCommand struct {
	ProductID string
}

// tag::entity_workflow[]
func CartWorkflow(ctx workflow.Context, cartID string) (*CartState, error) {
	state := &CartState{ID: cartID, UpdatedAt: workflow.Now(ctx)} // <1>

	err := workflow.SetQueryHandler(ctx, "getCart", func() (*CartState, error) { // <2>
		return state, nil
	})
	if err != nil {
		return nil, fmt.Errorf("register query handler: %w", err)
	}

	addItemCh := workflow.GetSignalChannel(ctx, "addItem")    // <3>
	removeItemCh := workflow.GetSignalChannel(ctx, "removeItem")
	checkoutCh := workflow.GetSignalChannel(ctx, "checkout")

	checkedOut := false

	for !checkedOut { // <4>
		selector := workflow.NewSelector(ctx)

		selector.AddReceive(addItemCh, func(c workflow.ReceiveChannel, _ bool) {
			var cmd AddItemCommand
			c.Receive(ctx, &cmd)
			state.Items = append(state.Items, cmd.Item) // <5>
			state.UpdatedAt = workflow.Now(ctx)
		})

		selector.AddReceive(removeItemCh, func(c workflow.ReceiveChannel, _ bool) {
			var cmd RemoveItemCommand
			c.Receive(ctx, &cmd)
			for i, item := range state.Items {
				if item.ProductID == cmd.ProductID {
					state.Items = append(state.Items[:i], state.Items[i+1:]...)
					break
				}
			}
			state.UpdatedAt = workflow.Now(ctx)
		})

		selector.AddReceive(checkoutCh, func(c workflow.ReceiveChannel, _ bool) {
			var signal struct{}
			c.Receive(ctx, &signal)
			checkedOut = true
		})

		selector.Select(ctx)

		if ctx.Err() != nil {
			return state, ctx.Err()
		}
	}

	return state, nil
}

// end::entity_workflow[]
