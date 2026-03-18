using Temporalio.Workflows;

namespace SagaExample.Workflows;

// tag::saga_workflow[]
[Workflow]
public class TravelBookingWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(BookingRequest request)
    {
        var compensations = new Stack<Func<Task>>();

        try
        {
            // Step 1: Reserve flight
            var flightRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ReserveFlightAsync(request.FlightId),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) });
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.CancelFlightAsync(flightRef),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) }));

            // Step 2: Reserve hotel
            var hotelRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ReserveHotelAsync(request.HotelId),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) });
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.CancelHotelAsync(hotelRef),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) }));

            // Step 3: Charge payment
            var paymentRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ChargePaymentAsync(request.PaymentInfo, request.TotalAmount),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(60) });
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.RefundPaymentAsync(paymentRef),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) }));

            return $"Booked: flight={flightRef}, hotel={hotelRef}, payment={paymentRef}";
        }
        catch (Exception ex)
        {
            // Compensate in reverse order
            while (compensations.Count > 0)
            {
                var compensation = compensations.Pop();
                await compensation();
            }

            return $"Booking failed and compensated: {ex.Message}";
        }
    }
}
// end::saga_workflow[]

public record BookingRequest(
    string FlightId,
    string HotelId,
    string PaymentInfo,
    decimal TotalAmount);
