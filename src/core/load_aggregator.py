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

        storage_values = [
            load.nf_storage_usage
            for load in load_level_info
            if load.nf_storage_usage is not None
        ]

        load_level_average_values = [
            load.nf_load_level_average
            for load in load_level_info
            if load.nf_load_level_average is not None
        ]

        load_level_peak_values = [
            load.nf_load_levelpeak
            for load in load_level_info
            if load.nf_load_levelpeak is not None
        ]

        load_avg_in_aoi_values = [
            load.nf_load_avg_in_aoi
            for load in load_level_info
            if load.nf_load_avg_in_aoi is not None
        ]

        cpu_usage = average(cpu_values)
        memory_usage = average(memory_values)
        storage_usage = average(storage_values)
        load_level_average = average(load_level_average_values)
        load_level_peak = average(load_level_peak_values)
        load_avg_in_aoi = average(load_avg_in_aoi_values)

        load = NfLoadLevelInformation()
        load.nf_type = load_level_info[0].nf_type
        load.nf_instance_id = instance_id
        load.nf_set_id = load_level_info[0].nf_set_id
        load.nf_status = load_level_info[0].nf_status

        load.nf_cpu_usage = int(cpu_usage)
        load.nf_memory_usage = int(memory_usage)
        load.nf_storage_usage = int(storage_usage)
        load.nf_load_level_average = int(load_level_average)
        load.nf_load_levelpeak = int(load_level_peak)
        load.nf_load_avg_in_aoi = int(load_avg_in_aoi)
        nf_load_level_infos.append(load)
    return nf_load_level_infos
