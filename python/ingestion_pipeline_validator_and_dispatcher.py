# You are designing a modular backend dispatch engine that validates 
# and processes incoming commands from multiple microservices.

# The dispatcher receives a batch of raw command payloads. 
# It must validate each payload against required fields, 
# enforce business constraints, convert data types safely, and route successful actions 
# while capturing structured error logs for bad requests,
# all without allowing any unhandled exceptions to crash the dispatcher.

raw_commands = [
    {"command_id": "cmd-101", "service": "billing", "action": "DEPOSIT", "amount": "250.75"},
    {"command_id": "cmd-102", "service": "billing", "action": "WITHDRAW", "amount": 100.0},
    {"command_id": "cmd-103", "service": "billing", "action": "REFUND", "amount": 50.0},        # Invalid action
    {"command_id": "cmd-104", "service": "",        "action": "DEPOSIT", "amount": 40.0},        # Empty service
    {"command_id": "cmd-105", "service": "billing", "action": "DEPOSIT", "amount": "-15.00"},    # Amount <= 0
    {"command_id": "cmd-106", "service": "billing", "action": "TRANSFER", "amount": "invalid"},  # Uncastable amount
    {"service": "billing", "action": "DEPOSIT", "amount": 10.0},                                 # Missing command_id
    {"command_id": "cmd-107", "service": "billing", "action": "TRANSFER", "amount": 500.0}
]

# Expected Output
{
    "summary": {
        "total": 8,
        "succeeded": 3,
        "failed": 5
    },
    "processed_commands": [
        {"command_id": "cmd-101", "service": "billing", "action": "DEPOSIT", "amount": 250.75},
        {"command_id": "cmd-102", "service": "billing", "action": "WITHDRAW", "amount": 100.0},
        {"command_id": "cmd-107", "service": "billing", "action": "TRANSFER", "amount": 500.0}
    ],
    "failed_commands": [
        {"command_id": "cmd-103", "error_type": "BusinessRuleViolationError", "reason": "Unsupported action: REFUND"},
        {"command_id": "cmd-104", "error_type": "ValidationError", "reason": "Service name cannot be empty"},
        {"command_id": "cmd-105", "error_type": "BusinessRuleViolationError", "reason": "Amount must be strictly positive"},
        {"command_id": "cmd-106", "error_type": "ValidationError", "reason": "Amount must be a numeric value"},
        {"command_id": "UNKNOWN", "error_type": "ValidationError", "reason": "Missing required field: command_id"}
    ]
}

class PipelineError(Exception):
    """Base Domain Exception"""
    pass

class ValidationError(PipelineError):
    """Raised for missing keys, empty strings, uncastable types, or booleans passed as numbers."""
    pass

class BusinessRuleViolationError(PipelineError):
    """Raised for invalid action strings or non-positive amounts."""
    pass

def validate_and_sanitize_command(cmd: dict) -> dict:
    keys = ("command_id", "service", "action", "amount")
    actions = ("DEPOSIT", "WITHDRAW", "TRANSFER")

    for key in keys:
        if key not in cmd: 
            raise ValidationError(f"Missing required field: {key}")

    command_id = str(cmd["command_id"]).strip()
    service = str(cmd["service"]).strip()
    if not command_id or not service:
        raise ValidationError(f"{"Command_id" if not command_id else "Service"} name cannot be empty") 

    action = cmd["action"]
    if action not in actions:
        raise BusinessRuleViolationError(f"Unsupported action: {cmd["action"]}")

    if isinstance(cmd["amount"], bool):
        raise ValidationError("Amount must be a numeric value")
    try:
        amount = float(cmd["amount"])
    except (ValueError, TypeError):
        raise ValidationError("Amount must be a numeric value")
    else:
        if amount <= 0:
            raise BusinessRuleViolationError("Amount must be strictly positive")

    return {
        "command_id": command_id,
        "service": service,
        "action": action,
        "amount": amount
    }

def dispatch_batch(cmds: list[dict]) -> dict:
    total = 0
    succeeded = 0
    failed= 0
    processed_commands, failed_commands = [], []

    for cmd in cmds:
        total+=1
        temp_dict = {}
        try:
            temp_dict = validate_and_sanitize_command(cmd)
        except PipelineError as exc:
            failed+=1
            failed_commands.append({
                "command_id": cmd.get("command_id", "UNKNOWN"),
                "error_type": type(exc).__name__,
                "reason": str(exc)
            })
        else:
            succeeded+=1
            processed_commands.append(temp_dict)

    return {
        "summary": {
            "total": total,
            "succeeded": succeeded,
            "failed": failed
        },
        "processed_commands": processed_commands,
        "failed_commands": failed_commands
    }


if __name__ == "__main__":
    print(dispatch_batch(raw_commands))