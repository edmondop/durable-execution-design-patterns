using HandlerService;
using Temporalio.Client;
using Temporalio.Testing;
using Temporalio.Worker;
using Xunit;

namespace HandlerService.Tests;

public class FulfillmentWorkflowTests
{
    [Fact]
    public async Task RunAsync_PicksAndShips_ReturnsTrackingNumber()
    {
        await using var env = await WorkflowEnvironment.StartTimeSkippingAsync();
        using var worker = new TemporalWorker(
            env.Client,
            new TemporalWorkerOptions("test-queue")
                .AddWorkflow<FulfillmentWorkflow>()
                .AddAllActivities(new WarehouseActivities()));

        await worker.ExecuteAsync(async () =>
        {
            var request = new FulfillmentRequest("order-abc12345", new List<string> { "item-1", "item-2" });
            var result = await env.Client.ExecuteWorkflowAsync(
                (FulfillmentWorkflow wf) => wf.RunAsync(request),
                new("fulfill-test-1", "test-queue"));

            Assert.StartsWith("TRACK-", result);
        });
    }
}
