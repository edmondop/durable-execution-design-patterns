using Temporalio.Activities;

namespace SagaExample.Workflows;

public class TravelActivities
{
    [Activity]
    public async Task<string> ReserveFlightAsync(string flightId)
    {
        Console.WriteLine($"Reserving flight {flightId}");
        return $"flight-ref-{flightId}";
    }

    [Activity]
    public async Task CancelFlightAsync(string flightRef)
    {
        Console.WriteLine($"Cancelling flight reservation {flightRef}");
    }

    [Activity]
    public async Task<string> ReserveHotelAsync(string hotelId)
    {
        Console.WriteLine($"Reserving hotel {hotelId}");
        return $"hotel-ref-{hotelId}";
    }

    [Activity]
    public async Task CancelHotelAsync(string hotelRef)
    {
        Console.WriteLine($"Cancelling hotel reservation {hotelRef}");
    }

    [Activity]
    public async Task<string> ChargePaymentAsync(string paymentInfo, decimal amount)
    {
        Console.WriteLine($"Charging {amount:C} via {paymentInfo}");
        return $"payment-ref-{Guid.NewGuid().ToString("N")[..8]}";
    }

    [Activity]
    public async Task RefundPaymentAsync(string paymentRef)
    {
        Console.WriteLine($"Refunding payment {paymentRef}");
    }
}
