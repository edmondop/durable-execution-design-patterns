package main

import (
	"log"

	entity "github.com/temporalio/durable-patterns/ch01-entity"
	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
)

func main() {
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalf("Unable to create client: %v", err)
	}
	defer c.Close()

	w := worker.New(c, "cart-task-queue", worker.Options{})

	w.RegisterWorkflow(entity.CartWorkflow)
	w.RegisterActivity(&entity.CartActivities{})

	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalf("Unable to start worker: %v", err)
	}
}
