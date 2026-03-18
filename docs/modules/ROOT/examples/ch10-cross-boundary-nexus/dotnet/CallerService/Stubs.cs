using Temporalio.Activities;

namespace CallerService;

public class OrderActivities
{
    [Activity]
    public async Task<string> CreateOrderAsync(OrderRequest request)
    {
        return await Task.FromResult($"order-{Guid.NewGuid().ToString("N")[..8]}");
    }
}

// tag::nexus_contract[]
public interface IFulfillmentService
{
    Task<string> FulfillOrderAsync(FulfillmentRequest request);
}
// end::nexus_contract[]
