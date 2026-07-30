
def max_drawdown_check(portfolio_value, peak):
    drawdown = (peak - portfolio_value) / peak

    if drawdown > 0.1:  # 10%
        return "STOP_TRADING"

    return "OK"
