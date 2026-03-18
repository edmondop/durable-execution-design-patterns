using Temporalio.Workflows;

namespace CallerService;

// tag::nexus_caller[]
[Workflow]
public class OrderWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(OrderRequest request)
    {
        // Process order locally
        var orderId = await Workflow.ExecuteActivityAsync(
            (OrderActivities a) => a.CreateOrderAsync(request),
            new() { StartToCloseTimeout = TimeSpan.FromSeconds(30) });

        // Cross-boundary call to Warehouse service via Nexus
        // The caller knows only the operation contract, not the handler's internals
        var nexusClient = Workflow.CreateNexusClient<IFulfillmentService>(
            new NexusClientOptions { Endpoint = "warehouse-nexus-endpoint" });

        var fulfillmentId = await nexusClient.ExecuteNexusOperationAsync(
            svc => svc.FulfillOrderAsync(new FulfillmentRequest(orderId, request.Items)),
            new() { ScheduleToCloseTimeout = TimeSpan.FromMinutes(30) });

        return $"Order {orderId} fulfilled: {fulfillmentId}";
    }
}
// end::nexus_caller[]

public record OrderRequest(string CustomerId, List<string> Items);
public record FulfillmentRequest(string OrderId, List<string> Items);
