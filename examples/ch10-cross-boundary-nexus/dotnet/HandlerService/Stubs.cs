using Temporalio.Activities;

namespace HandlerService;

public class WarehouseActivities
{
    [Activity]
    public async Task PickItemsAsync(string orderId, List<string> items)
    {
        Console.WriteLine($"Picking {items.Count} items for order {orderId}");
    }

    [Activity]
    public async Task<string> ShipPackageAsync(string orderId)
    {
        return $"TRACK-{orderId[..8]}";
    }
}
