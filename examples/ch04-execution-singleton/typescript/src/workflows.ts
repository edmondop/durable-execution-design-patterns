import { proxyActivities, sleep } from '@temporalio/workflow';
import type * as activities from './activities';

const { processPayment, markPaymentComplete } = proxyActivities<typeof activities>({
  startToCloseTimeout: '30s',
});

// tag::execution_singleton[]
/**
 * Payment processing workflow. The workflow ID is `payment-${paymentId}`,
 * so the runtime guarantees at most one active execution per payment.
 *
 * If a second start request arrives for the same payment ID, the runtime
 * returns the existing execution — no duplicate processing.
 */
export async function paymentWorkflow(paymentId: string, amount: number): Promise<string> {
  // Process the payment — this runs exactly once per payment ID
  const transactionId = await processPayment(paymentId, amount);

  // Simulate some post-processing delay
  await sleep('5s');

  // Mark as complete
  await markPaymentComplete(paymentId, transactionId);

  return transactionId;
}
// end::execution_singleton[]
