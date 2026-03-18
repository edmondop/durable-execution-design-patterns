package main

import (
	"encoding/json"
	"log"
	"net/http"

	entity "github.com/temporalio/durable-patterns/ch01-entity"
	"go.temporal.io/sdk/client"
)

var temporalClient client.Client

func main() {
	var err error
	temporalClient, err = client.Dial(client.Options{})
	if err != nil {
		log.Fatalf("Unable to create client: %v", err)
	}
	defer temporalClient.Close()

	http.HandleFunc("GET /carts/{id}", getCart)
	http.HandleFunc("POST /carts/{id}/items", addItem)
	http.HandleFunc("DELETE /carts/{id}/items/{productId}", removeItem)
	http.HandleFunc("POST /carts/{id}/checkout", checkout)

	log.Println("API server listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func getCart(w http.ResponseWriter, r *http.Request) {
	cartID := r.PathValue("id")
	resp, err := temporalClient.QueryWorkflow(r.Context(), "cart-"+cartID, "", "getCart")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var state entity.CartState
	if err := resp.Get(&state); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(state)
}

func addItem(w http.ResponseWriter, r *http.Request) {
	cartID := r.PathValue("id")
	var item entity.CartItem
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err := temporalClient.SignalWorkflow(r.Context(), "cart-"+cartID, "",
		"addItem", entity.AddItemCommand{Item: item})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusAccepted)
}

func removeItem(w http.ResponseWriter, r *http.Request) {
	cartID := r.PathValue("id")
	productID := r.PathValue("productId")

	err := temporalClient.SignalWorkflow(r.Context(), "cart-"+cartID, "",
		"removeItem", entity.RemoveItemCommand{ProductID: productID})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusAccepted)
}

func checkout(w http.ResponseWriter, r *http.Request) {
	cartID := r.PathValue("id")

	err := temporalClient.SignalWorkflow(r.Context(), "cart-"+cartID, "",
		"checkout", struct{}{})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusAccepted)
}
