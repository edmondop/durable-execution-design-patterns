using SagaExample.Workflows;
using Temporalio.Client;
using Temporalio.Testing;
using Temporalio.Worker;
using Xunit;

namespace SagaExample.Tests;

public class TravelBookingWorkflowTests
{
    [Fact]
    public async Task RunAsync_AllSucceed_ReturnsBookingConfirmation()
    {
        await using var env = await WorkflowEnvironment.StartTimeSkippingAsync();
        using var worker = new TemporalWorker(
            env.Client,
            new TemporalWorkerOptions("test-queue")
                .AddWorkflow<TravelBookingWorkflow>()
                .AddAllActivities(new TravelActivities()));

        await worker.ExecuteAsync(async () =>
        {
            var request = new BookingRequest("FL-100", "HT-200", "CC-1234", 500m);
            var result = await env.Client.ExecuteWorkflowAsync(
                (TravelBookingWorkflow wf) => wf.RunAsync(request),
                new("travel-test-1", "test-queue"));

            Assert.Contains("Booked:", result);
            Assert.Contains("flight=", result);
            Assert.Contains("hotel=", result);
            Assert.Contains("payment=", result);
        });
    }
}
