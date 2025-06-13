from typing import Dict
from pydantic import StrictInt


from openapi_server.models.nf_load_level_information import NfLoadLevelInformation


def average(values: list[StrictInt]) -> float:
    return round(sum(values) / len(values), 2) if values else 0


def aggregate(
    nf_load_level_infos_by_instance: Dict[str, list[NfLoadLevelInformation]],
) -> list[NfLoadLevelInformation]:

    nf_load_level_infos = []
    for instance_id, load_level_info in nf_load_level_infos_by_instance.items():
        if not load_level_info:
            continue
        cpu_values = [
            load.nf_cpu_usage
            for load in load_level_info
            if load.nf_cpu_usage is not None
        ]

        memory_values = [
            load.nf_memory_usage
            for load in load_level_info
            if load.nf_memory_usage is not None
        ]

        cpu_usage = average(cpu_values)
        memory_usage = average(memory_values)

        load = NfLoadLevelInformation()
        load.nf_type = load_level_info[0].nf_type
        load.nf_instance_id = instance_id
        load.nf_cpu_usage = int(cpu_usage)
        load.nf_memory_usage = int(memory_usage)
        nf_load_level_infos.append(load)
    return nf_load_level_infos
