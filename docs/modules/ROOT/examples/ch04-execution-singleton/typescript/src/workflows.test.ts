import { TestWorkflowEnvironment } from '@temporalio/testing';
import { Worker } from '@temporalio/worker';

describe('paymentWorkflow', () => {
  let testEnv: TestWorkflowEnvironment;

  beforeAll(async () => {
    testEnv = await TestWorkflowEnvironment.createTimeSkipping();
  });

  afterAll(async () => {
    await testEnv?.teardown();
  });

  it('processes payment and returns transaction ID', async () => {
    const worker = await Worker.create({
      connection: testEnv.nativeConnection,
      taskQueue: 'test',
      workflowsPath: require.resolve('./workflows'),
      activities: {
        processPayment: async (paymentId: string, _amount: number) => `txn-${paymentId}`,
        markPaymentComplete: async () => {},
      },
    });

    const result = await worker.runUntil(
      testEnv.client.workflow.execute('paymentWorkflow', {
        args: ['pay-001', 100.0],
        workflowId: 'payment-pay-001',
        taskQueue: 'test',
      })
    );

    expect(result).toBe('txn-pay-001');
  });
});
