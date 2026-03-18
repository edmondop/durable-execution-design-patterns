import {
  condition,
  defineSignal,
  defineQuery,
  setHandler,
  sleep,
} from '@temporalio/workflow';

interface FraudEvent {
  type: 'login' | 'transaction' | 'location_change' | 'device_change';
  timestamp: number;
  details: Record<string, unknown>;
}

interface AlertResult {
  triggered: boolean;
  reason: string;
  events: FraudEvent[];
}

export const reportEvent = defineSignal<[FraudEvent]>('reportEvent');
export const getStatus = defineQuery<AlertResult>('getStatus');

// tag::durable_observer[]
export async function fraudMonitorWorkflow(accountId: string): Promise<AlertResult> {
  const events: FraudEvent[] = [];
  let alertTriggered = false;
  let alertReason = '';

  // Register signal handler for incoming events
  setHandler(reportEvent, (event: FraudEvent) => {
    events.push(event);

    // Correlation rule: new device + large transaction within 5 minutes
    const recentDeviceChange = events.find(
      (e) =>
        e.type === 'device_change' &&
        event.timestamp - e.timestamp < 5 * 60 * 1000,
    );

    if (
      event.type === 'transaction' &&
      recentDeviceChange &&
      (event.details.amount as number) > 1000
    ) {
      alertTriggered = true;
      alertReason = `Large transaction ($${event.details.amount}) from new device within 5 minutes`;
    }
  });

  setHandler(getStatus, () => ({
    triggered: alertTriggered,
    reason: alertReason,
    events,
  }));

  // Wait for alert or monitoring window expiry (24 hours)
  await condition(() => alertTriggered, '24h');

  return {
    triggered: alertTriggered,
    reason: alertReason || 'Monitoring window expired without alert',
    events,
  };
}
// end::durable_observer[]
