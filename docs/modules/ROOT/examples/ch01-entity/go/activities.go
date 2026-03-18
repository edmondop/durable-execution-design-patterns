package entity

import (
	"context"
	"fmt"
)

// tag::entity_activities[]
type CartActivities struct{}

func (a *CartActivities) SendOrderConfirmation(ctx context.Context, state *CartState) error {
	fmt.Printf("Order confirmed for cart %s: %d items, total $%.2f\n",
		state.ID, len(state.Items), state.Total())
	return nil
}

func (a *CartActivities) ReserveInventory(ctx context.Context, items []CartItem) error {
	for _, item := range items {
		fmt.Printf("Reserved: %s x%d\n", item.Name, item.Quantity)
	}
	return nil
}

// end::entity_activities[]
