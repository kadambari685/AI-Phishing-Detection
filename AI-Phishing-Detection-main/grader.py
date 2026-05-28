def grade_phishing_task(agent_output: str, expected_output: str) -> float:
    """
    Evaluates the agent's action against the ground truth.
    Returns a score between 0.0 and 1.0.
    """
    # Normalize inputs to avoid case-sensitivity issues
    agent_action = agent_output.strip().upper()
    expected_action = expected_output.strip().upper()

    # Perfect match: Maximum reward
    if agent_action == expected_action:
        return 1.0
    
    # Partial credit: If agent quarantined instead of blocking (safe but cautious)
    if agent_action == "QUARANTINE" and expected_action == "BLOCK_DOMAIN":
        return 0.5
        
    # Failure: Incorrect categorization or allowing a threat
    return 0.0

def calculate_overall_score(task_scores: list) -> float:
    """
    Calculates the final reproducible score for the baseline report.
    """
    if not task_scores:
        return 0.0
    return sum(task_scores) / len(task_scores)