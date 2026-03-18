package io.temporal.patterns.perpetual;

import io.temporal.activity.ActivityInterface;

@ActivityInterface
public interface BillingActivities {

    void chargeSubscription(String subscriptionId, double amount);

    void sendReceipt(String subscriptionId, String email);
}
