from evaluation_engine.evaluation_models import Severity, EvaluationSummary, EvaluationMessage


class BaseEvaluator:
    @classmethod
    def _highest_severity(cls, messages):
        if not messages:
            return None

        priority = {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3
        }

        return max(
            (message.severity for message in messages),
            key=lambda severity: priority[severity]
        )
    
    @classmethod
    def _build_summary(cls, messages):
        return EvaluationSummary(
            message_count=len(messages),
            highest_severity=cls._highest_severity(messages)
        )
    
    @classmethod
    def collect_messages(cls, *messages):
        return [message for message in messages if message is not None]
    
    @classmethod
    def message(cls, code, type, severity, message):
        return EvaluationMessage(
            code=code,
            type=type,
            severity=severity,
            message=message
        )
    
    @classmethod
    def build_result(cls, result_class, **kwargs):
        kwargs["summary"] = cls._build_summary(kwargs["messages"])
        return result_class(**kwargs)