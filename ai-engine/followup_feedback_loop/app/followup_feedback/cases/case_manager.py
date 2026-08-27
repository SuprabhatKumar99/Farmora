from app.followup_feedback.schemas.models import FollowUpCase, FollowUpStatus


class FollowUpCaseManager:
    """Manage follow-up case state without directly changing production
    decisions, model weights, or knowledge-base records.
    """

    ALLOWED = {
        FollowUpStatus.CREATED: {
            FollowUpStatus.SCHEDULED,
            FollowUpStatus.OBSERVATION_RECEIVED,
            FollowUpStatus.CLOSED,
        },
        FollowUpStatus.SCHEDULED: {
            FollowUpStatus.OBSERVATION_RECEIVED,
            FollowUpStatus.CLOSED,
        },
        FollowUpStatus.OBSERVATION_RECEIVED: {
            FollowUpStatus.OUTCOME_RECORDED,
            FollowUpStatus.VALIDATED,
            FollowUpStatus.CLOSED,
        },
        FollowUpStatus.OUTCOME_RECORDED: {
            FollowUpStatus.VALIDATED,
            FollowUpStatus.CLOSED,
        },
        FollowUpStatus.VALIDATED: {
            FollowUpStatus.CLOSED,
        },
        FollowUpStatus.CLOSED: set(),
    }

    def transition(self, case: FollowUpCase, new_status: FollowUpStatus):
        if new_status == case.status:
            return case

        if new_status not in self.ALLOWED[case.status]:
            raise ValueError(
                f"INVALID_FOLLOWUP_TRANSITION:{case.status}->{new_status}"
            )

        case.status = new_status
        return case
