import { TestWorkflowEnvironment } from '@temporalio/testing';
import { Worker } from '@temporalio/worker';
import { fraudMonitorWorkflow, reportEvent } from './workflows';

describe('fraudMonitorWorkflow', () => {
  let testEnv: TestWorkflowEnvironment;

  beforeAll(async () => {
    testEnv = await TestWorkflowEnvironment.createTimeSkipping();
  });

  afterAll(async () => {
    await testEnv?.teardown();
  });

  it('triggers alert on device change followed by large transaction', async () => {
    const worker = await Worker.create({
      connection: testEnv.nativeConnection,
      taskQueue: 'test',
      workflowsPath: require.resolve('./workflows'),
    });

    const result = await worker.runUntil(async () => {
      const handle = await testEnv.client.workflow.start(fraudMonitorWorkflow, {
        args: ['acct-001'],
        workflowId: 'fraud-acct-001',
        taskQueue: 'test',
      });

      const now = Date.now();

      await handle.signal(reportEvent, {
        type: 'device_change',
        timestamp: now,
        details: { device: 'new-phone' },
      });

      await handle.signal(reportEvent, {
        type: 'transaction',
        timestamp: now + 60_000,
        details: { amount: 5000 },
      });

      return handle.result();
    });

    expect(result.triggered).toBe(true);
    expect(result.reason).toContain('Large transaction');
    expect(result.events).toHaveLength(2);
  });
});
