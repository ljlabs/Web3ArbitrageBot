from dis import Instruction


class TradeInstruction:

    exchange: str
    path: list[str]
    inpt: int
    outpt: int

    def __init__(self, exchange, path, inpt, outpt):
        self.exchange = exchange
        self.path = path
        self.inpt = inpt
        self.outpt = outpt

    def params(self):
        return (self.exchange, self.path, self.inpt, self.outpt)

    @staticmethod
    def transform(circuit):
        instructions = []
        past_exchange = None
        path = []
        for pair in circuit:
            tok_a = pair.split("_")[0]
            tok_b = pair.split("_")[1]
            dex = pair.split("_")[2]
            if dex != past_exchange:
                if past_exchange is not None:
                    instructions.append(TradeInstruction(
                        past_exchange, path, 0, 0))
                    path = []
                path.append(tok_a)
                path.append(tok_b)
            else:
                path.append(tok_b)
            past_exchange = dex
        instructions.append(TradeInstruction(past_exchange, path, 0, 0))
        return instructions

    @staticmethod
    def set_price(trade_instructions, min_output):
        for i in range(len(trade_instructions)):
            trade_instructions[i].inpt = min_output[i][0]
            trade_instructions[i].outpt = min_output[i][-1]
        return trade_instructions
