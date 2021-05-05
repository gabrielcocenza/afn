# Gabriel Angelo Sgarbi Cocenza nºUSP: 6448118

import traceback
import logging

from nfa import NFA
from typing import List

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


def read_chain_file() -> List:
    with open("entrada.txt", "r") as f:
        return f.read().splitlines()


def write_output_file(results) -> None:
    with open("saida.txt", "w") as f:
        for result in results:
            f.write(" ".join(result))


def build_nfa(lines: List, automata_index: int) -> NFA:
    automata_info = [int(x) for x in lines[automata_index].split(" ")]
    states = set(str(i) for i in range(automata_info[0]))
    input_symbols = set([str(i) for i in range(automata_info[1])])
    n_transitions = int(automata_info[2])
    initial_state = str(automata_info[3])
    final_states = set([x for x in lines[automata_index + 1].split(" ")])

    transitions = {}
    for i in range(n_transitions):
        t = lines[automata_index + 2 + i].split(" ")
        state_begin = t[0]
        input_symbol = t[1]
        state_end = t[2]
        if not transitions.get(state_begin):
            transitions[state_begin] = {}
        if not transitions[state_begin].get(input_symbol):
            transitions[state_begin][input_symbol] = set()
        transitions[state_begin][input_symbol].add(state_end)

    return (
        NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        ),
        n_transitions,
    )


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    results = []
    current_automata = 1
    automata_index = 1
    lines = read_chain_file()
    n_automata = int(lines[0])

    while current_automata <= n_automata:
        nfa, n_transitions = build_nfa(lines, automata_index)
        n_inputs = int(lines[automata_index + 2 + n_transitions])
        inputs = [
            lines[automata_index + 3 + n_transitions + i].replace(" ", "")
            for i in range(n_inputs)
        ]

        LOGGER.info(
            f"""
            Autômato_{current_automata}:
            States: {nfa.states}
            Input Symbols: {nfa.input_symbols}
            Transitions: {nfa.transitions}
            Initial State: {nfa.initial_state}
            Final States: {nfa.final_states}
            Inputs: {inputs}
        """
        )

        result = []
        for input in inputs:
            try:
                nfa.read_chain(input)
                result.append("1")
            except Exception as e:
                LOGGER.error(e)
                result.append("0")

        results.append(result + ["\n"])

        LOGGER.info(f"""Result: {result}""")
        automata_index = automata_index + n_transitions + n_inputs + 3
        current_automata += 1

    write_output_file(results)


if __name__ == "__main__":
    main()
