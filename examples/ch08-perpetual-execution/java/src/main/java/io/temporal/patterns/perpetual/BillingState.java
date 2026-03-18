package io.temporal.patterns.perpetual;

public record BillingState(
    String subscriptionId,
    String email,
    double amount,
    int cycleCount
) {}
