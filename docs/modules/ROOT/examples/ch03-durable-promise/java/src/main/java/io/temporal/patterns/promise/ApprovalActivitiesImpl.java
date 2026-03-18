package io.temporal.patterns.promise;

public class ApprovalActivitiesImpl implements ApprovalActivities {

    @Override
    public void sendApprovalRequest(ApprovalRequest request) {
        System.out.printf("Sending approval request %s to %s for $%.2f%n",
                request.requestId(), request.approver(), request.amount());
    }

    @Override
    public void processApproval(ApprovalRequest request) {
        System.out.printf("Processing approval for request %s%n", request.requestId());
    }

    @Override
    public void processRejection(ApprovalRequest request) {
        System.out.printf("Processing rejection for request %s%n", request.requestId());
    }

    @Override
    public void sendDeadlineExpired(ApprovalRequest request) {
        System.out.printf("Deadline expired for request %s%n", request.requestId());
    }
}
