from game_types.game_types import AttemptResult, AttemptResultStatus, GameStatus
from typing import List


def get_number_of_mistakes(attempts: List[AttemptResult]) -> int:
    """Return the number of mistakes in the given attempts."""
    # an attempt is a mistake if it wasnt a success
    return len(
        [
            attempt
            for attempt in attempts
            if attempt.result != AttemptResultStatus.SUCCESS
        ]
    )


def get_number_of_correct_groups(attempts: List[AttemptResult]) -> int:
    """Return the number of correct groups in the given attempts."""
    # an attempt is a correct group if it was a success
    correct_attempt_results = filter(
        lambda attempt: attempt.result == AttemptResultStatus.SUCCESS,
        attempts,
    )
    return len(list(correct_attempt_results))


def get_game_over_message(
    game_id: int, attempts: List[AttemptResult], game_status: GameStatus
) -> str:
    """Return a summary message for the game being over."""

    number_of_attempts = len(attempts)
    mistakes = get_number_of_mistakes(attempts)
    correct_groups = get_number_of_correct_groups(attempts)
    game_summary = f"Game {str(game_id)} over! {game_status.name} in {number_of_attempts} attempts with {mistakes} mistakes and {correct_groups} correct groups."
    for i, attempt in enumerate(attempts):
        game_summary += f"\n\t{i+1}. {attempt.pretty_str()}"
    return game_summary
