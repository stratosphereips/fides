import concurrent
import random
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

from fides.evaluation.ti_aggregation import AverageConfidenceTIAggregation, \
    WeightedAverageConfidenceTIAggregation
from fides.evaluation.ti_evaluation import MaxConfidenceTIEvaluation, DistanceBasedTIEvaluation, ThresholdTIEvaluation
from fides.utils.logger import Logger, LoggerPrintCallbacks
from simulations.environment import generate_and_run
from simulations.peer import PeerBehavior
from simulations.setup import SimulationConfiguration
from simulations.storage import store_simulation_result

logger = Logger(__name__)
sims_number = 0


def append_if_possible(row, value) -> bool:
    if sum(row) + value <= 1:
        row.append(value)
        return True
    else:
        return False


def sample_peers_distribution() -> List[List[float]]:
    # [CONFIDENT_CORRECT, UNCERTAIN_PEER, CONFIDENT_INCORRECT, MALICIOUS]

    sample = {
        'cc': [0.0, 0.25, 0.5, 0.75],
        'up': [0.0, 0.25, 0.5, 0.75],
        'ci': [0.0, 0.25, 0.5, 0.75],
        'ma': [0.0, 0.25, 0.5, 0.75],
    }
    data = []
    for cc in sample['cc']:
        row = [cc]
        for up in sample['up']:
            if not append_if_possible(row, up):
                continue
            for ci in sample['ci']:
                if not append_if_possible(row, ci):
                    continue
                for ma in sample['ma']:
                    if not append_if_possible(row, ma):
                        continue
                    if sum(row) == 1:
                        data.append(row)
                    row = row[:-1]
                row = row[:-1]
            row = row[:-1]
    return data


def sample_simulation_definitions() -> List[SimulationConfiguration]:
    peers_count = [8]
    pre_trusted_peers = [0.0, 0.25, 0.5, 0.75]

    # CC,  UP,  CI,  MA
    peers_distribution = sample_peers_distribution()

    targets = [2]
    malicious_targets = [0.5]
    malicious_peers_lie_abouts = [1.0]
    gaining_trust_periods = [50]

    simulation_lengths = [200]
    service_history_sizes = [100]
    evaluation_strategies = [
        MaxConfidenceTIEvaluation(),
        DistanceBasedTIEvaluation(),
        ThresholdTIEvaluation(threshold=0.5),
    ]
    ti_aggregation_strategies = [
        AverageConfidenceTIAggregation(),
        WeightedAverageConfidenceTIAggregation(),
    ]
    initial_reputations = [0.0, 0.5, 0.95]
    local_slips_acts_ass = [PeerBehavior.CONFIDENT_CORRECT,
                            PeerBehavior.UNCERTAIN_PEER]

    ns = len(peers_count) * len(peers_distribution) * len(pre_trusted_peers) * len(targets) * \
         len(malicious_targets) * len(malicious_peers_lie_abouts) * \
         len(gaining_trust_periods) * len(simulation_lengths) * len(service_history_sizes) * \
         len(evaluation_strategies) * len(ti_aggregation_strategies) * \
         len(initial_reputations) * len(local_slips_acts_ass)
    logger.warn(f'Original number of combinations: {ns}')

    simulations = []
    for peer_count in peers_count:
        for distribution in peers_distribution:
            p_distribution = {
                PeerBehavior.CONFIDENT_CORRECT: round(distribution[0] * peer_count),
                PeerBehavior.UNCERTAIN_PEER: round(distribution[1] * peer_count),
                PeerBehavior.CONFIDENT_INCORRECT: round(distribution[2] * peer_count),
                PeerBehavior.MALICIOUS_PEER: round(distribution[3] * peer_count)
            }
            p_distribution[PeerBehavior.UNCERTAIN_PEER] = \
                peer_count - p_distribution[PeerBehavior.CONFIDENT_CORRECT] - \
                p_distribution[PeerBehavior.CONFIDENT_INCORRECT] - \
                p_distribution[PeerBehavior.MALICIOUS_PEER]
            for pre_trusted_peer in pre_trusted_peers:
                if pre_trusted_peer < distribution[0]:
                    continue
                for target in targets:
                    for malicious_target in malicious_targets:
                        malicious_targets_count = int(target * malicious_target)
                        being_targets_count = target - malicious_targets_count
                        for malicious_peers_lie_about in malicious_peers_lie_abouts:
                            for gaining_trust_period in gaining_trust_periods:
                                for simulation_length in simulation_lengths:
                                    for service_history_size in service_history_sizes:
                                        for evaluation_strategy in evaluation_strategies:
                                            for ti_aggregation_strategy in ti_aggregation_strategies:
                                                for initial_reputation in initial_reputations:
                                                    for local_slips_acts_as in local_slips_acts_ass:
                                                        simulation_configuration = SimulationConfiguration(
                                                            benign_targets=being_targets_count,
                                                            malicious_targets=malicious_targets_count,
                                                            malicious_peers_lie_about_targets=malicious_peers_lie_about,
                                                            peers_distribution=p_distribution,
                                                            simulation_length=simulation_length,
                                                            malicious_peers_lie_since=gaining_trust_period,
                                                            service_history_size=service_history_size,
                                                            pre_trusted_peers_count=int(peer_count * pre_trusted_peer),
                                                            initial_reputation=initial_reputation,
                                                            local_slips_acts_as=local_slips_acts_as,
                                                            evaluation_strategy=evaluation_strategy,
                                                            ti_aggregation_strategy=ti_aggregation_strategy,
                                                        )
                                                        simulations.append(simulation_configuration)
    return simulations


def log_callback(level: str, msg: str):
    if level in {'ERROR', 'WARN'}:
        print(f'{level}: {msg}\n')


def execute_configuration(i: Tuple[int, SimulationConfiguration]):
    try:
        LoggerPrintCallbacks[0] = log_callback
        idx, configuration = i
        logger.warn(f'#{idx}/{sims_number} - executing')
        result = generate_and_run(configuration)
        store_simulation_result(f'results/{result.simulation_id}.json', result)
        logger.warn(f'#{idx}/{sims_number} - done id {result.simulation_id}')
    except Exception as ex:
        logger.error("error during execution", ex)


if __name__ == '__main__':
    sims = sample_simulation_definitions()
    random.shuffle(sims)

    logger.warn(f"Generated number of simulations: {len(sims)}")
    sims_number = len(sims)
    enumerated_sims = [(idx, sim) for idx, sim in enumerate(sims)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(execute_configuration, enumerated_sims)

    logger.warn("Simulations done")
