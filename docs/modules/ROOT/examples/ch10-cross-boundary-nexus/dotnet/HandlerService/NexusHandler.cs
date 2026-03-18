using Temporalio.Workflows;

namespace HandlerService;

// tag::nexus_handler[]
[Workflow]
public class FulfillmentWorkflow
{
    [WorkflowRun]
    public async Task<string> RunAsync(FulfillmentRequest request)
    {
        // Pick items from warehouse
        await Workflow.ExecuteActivityAsync(
            (WarehouseActivities a) => a.PickItemsAsync(request.OrderId, request.Items),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(10) });

        // Pack and ship
        var trackingNumber = await Workflow.ExecuteActivityAsync(
            (WarehouseActivities a) => a.ShipPackageAsync(request.OrderId),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });

        return trackingNumber;
    }
}
// end::nexus_handler[]

public record FulfillmentRequest(string OrderId, List<string> Items);
