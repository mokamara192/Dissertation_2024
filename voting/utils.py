def calculate_percentage(votes):
    total_votes = sum(votes)
    percentages = [(vote / total_votes) * 100 if total_votes != 0 else 0 for vote in votes]
    return percentages