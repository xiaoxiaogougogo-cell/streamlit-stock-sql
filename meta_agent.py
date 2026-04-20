def meta_decision(signals):



    score = 0



    for s in signals:



        if s == "BUY":



            score += 1



        elif s == "SELL":



            score -= 1



    if score >= 2:



        return "BUY"



    elif score <= -2:



        return "SELL"



    return "HOLD"








#🤖 3. Multi-agent system (ML + RL + rules)



def run_agents(ml_signal, rl_signal, rule_signal):



    return meta_decision([



        ml_signal,



        rl_signal,



        rule_signal



    ])
