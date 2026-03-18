package scattergather

import (
	"context"
	"fmt"
	"math/rand"
)

func SearchAirline(ctx context.Context, airline string, req PriceRequest) (*PriceResult, error) {
	price := 200.0 + rand.Float64()*500.0
	fmt.Printf("Searched %s: %s->%s on %s = $%.2f\n", airline, req.Origin, req.Dest, req.Date, price)
	return &PriceResult{
		Airline: airline,
		Price:   price,
	}, nil
}
