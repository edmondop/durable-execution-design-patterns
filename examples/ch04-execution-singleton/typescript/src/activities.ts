export async function processPayment(paymentId: string, amount: number): Promise<string> {
  console.log(`Processing payment ${paymentId} for $${amount}`);
  return `txn-${paymentId}-${Date.now()}`;
}

export async function markPaymentComplete(paymentId: string, transactionId: string): Promise<void> {
  console.log(`Payment ${paymentId} complete: ${transactionId}`);
}
