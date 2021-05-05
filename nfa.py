import abc
import copy
import logging


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -10s %(funcName) "
    "-20s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class AutomatonException(Exception):
    """The base class for all automaton-related errors."""
    pass

class RejectionException(AutomatonException):
    """The input was rejected by the automaton."""
    pass



class NFA:
    """A non deterministic finite automaton."""

    def __init__(self, states, input_symbols, transitions, initial_state, final_states):
        """Initialize the NFA with copies to not change the original object."""
        self.states = states.copy()
        self.input_symbols = input_symbols.copy()
        self.transitions = copy.deepcopy(transitions)
        self.initial_state = initial_state
        self.final_states = final_states.copy()

    def _get_lambda_state(self, start_state):
        """
        Check every state that can be reached from q(n) by lambda
        transitions.
        0 is represented as lambda in the automaton
        """
        stack = []
        encountered_states = set()
        stack.append(start_state)

        LOGGER.info(f"start_state: {start_state}")

        while stack:
            state = stack.pop()
            LOGGER.info(f"state: {state}")
            if state not in encountered_states:
                encountered_states.add(state)
                transitions_state = self.transitions.get(state)
                if transitions_state and "0" in transitions_state:
                    stack.extend(self.transitions[state]["0"])

        LOGGER.info(f"encountered_states: {encountered_states}")
        return encountered_states

    def _get_next_current_states(self, current_states, input_symbol):
        """Return the next set of current states given the current set."""
        next_current_states = set()

        LOGGER.info(f"current_states: {current_states} input_symbol: {input_symbol}")
        for current_state in current_states:
            symbol_end_states = self.transitions.get(current_state)
            if symbol_end_states:
                if symbol_end_states.get(input_symbol):
                    for end_state in symbol_end_states.get(input_symbol):
                        next_current_states.update(self._get_lambda_state(end_state))

        return next_current_states

    def _check_for_input_rejection(self, current_states):
        """Raises error if current states is not in final states"""
        if not (current_states & self.final_states):
            raise RejectionException(
                "the NFA stopped on all non-final states ({})".format(
                    ", ".join(str(state) for state in current_states)
                )
            )

    def read_chain(self, input_str: str):
        """
        Check if the given string is accepted by this automaton.
        Returns finals possibles states.
        """
        LOGGER.info(f"transitions: {self.transitions}")
        LOGGER.info(f"input_str: {input_str}")
        validation_generator = self.read_chain_step(input_str)
        for config in validation_generator:
            pass
        LOGGER.info(f"config: {config} \n\n")
        return config

    def read_chain_step(self, input_str: str):
        """
        Check if the string chain is accepted by the NFA.
        Yield the current configuration of the NFA at each step.
        """
        current_states = self._get_lambda_state(self.initial_state)

        yield current_states
        for input_symbol in input_str:
            current_states = self._get_next_current_states(current_states, input_symbol)
            yield current_states

        self._check_for_input_rejection(current_states)
