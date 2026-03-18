package io.temporal.patterns.promise;

public record ApprovalRequest(
    String requestId,
    String submitter,
    String approver,
    String description,
    double amount,
    int deadlineDays
) {}
