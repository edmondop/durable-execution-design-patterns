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
  const transactionId = await processPayment(paymentId, amount); // <1>

  await sleep('5s'); // <2>

  await markPaymentComplete(paymentId, transactionId); // <3>

  return transactionId; // <4>
}
// end::execution_singleton[]
