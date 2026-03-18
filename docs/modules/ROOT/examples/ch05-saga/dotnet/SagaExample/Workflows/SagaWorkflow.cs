using Temporalio.Common;
using Temporalio.Workflows;

namespace SagaExample.Workflows;

// tag::saga_workflow[]
[Workflow]
public class TravelBookingWorkflow
{
    private static readonly ActivityOptions ForwardOptions = new()
    {
        StartToCloseTimeout = TimeSpan.FromSeconds(30),
    };

    private static readonly ActivityOptions CompensationOptions = new()
    {
        StartToCloseTimeout = TimeSpan.FromSeconds(30),
        RetryPolicy = new RetryPolicy
        {
            MaximumAttempts = 10,
            InitialInterval = TimeSpan.FromSeconds(1),
            BackoffCoefficient = 2.0,
        },
    };

    [WorkflowRun]
    public async Task<string> RunAsync(BookingRequest request)
    {
        var compensations = new Stack<Func<Task>>();

        try
        {
            // Step 1: Reserve flight
            var flightRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ReserveFlightAsync(request.FlightId),
                ForwardOptions);
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.CancelFlightAsync(flightRef),
                CompensationOptions));

            // Step 2: Reserve hotel
            var hotelRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ReserveHotelAsync(request.HotelId),
                ForwardOptions);
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.CancelHotelAsync(hotelRef),
                CompensationOptions));

            // Step 3: Charge payment
            var paymentRef = await Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.ChargePaymentAsync(request.PaymentInfo, request.TotalAmount),
                new() { StartToCloseTimeout = TimeSpan.FromSeconds(60) });
            compensations.Push(() => Workflow.ExecuteActivityAsync(
                (TravelActivities a) => a.RefundPaymentAsync(paymentRef),
                CompensationOptions));

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
