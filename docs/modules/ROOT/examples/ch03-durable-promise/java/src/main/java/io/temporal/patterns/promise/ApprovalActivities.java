package io.temporal.patterns.promise;

import io.temporal.activity.ActivityInterface;

@ActivityInterface
public interface ApprovalActivities {

    void sendApprovalRequest(ApprovalRequest request);

    void processApproval(ApprovalRequest request);

    void processRejection(ApprovalRequest request);

    void sendDeadlineExpired(ApprovalRequest request);
}
