# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription  # noqa: F401
from openapi_server.models.problem_details import ProblemDetails  # noqa: F401
from openapi_server.models.redirect_response import RedirectResponse  # noqa: F401


def test_delete_ncof_events_subscription(client: TestClient):
    """Test case for delete_ncof_events_subscription

    Delete an existing Individual NCOF Events Subscription
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/subscriptions/{subscriptionId}".format(subscriptionId='subscription_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_ncof_events_subscription(client: TestClient):
    """Test case for update_ncof_events_subscription

    Update an existing Individual NCOF Events Subscription
    """
    nncof_events_subscription = {"supported_features":"supportedFeatures","notification_uri":"notificationURI","prev_sub":"prevSub","notif_corr_id":"notifCorrId","event_notifications":[{"nf_load_level_infos":[{"nf_instance_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","snssai":{"sd":"sd","sst":37},"nf_storage_usage":3,"nf_load_levelpeak":1,"nf_status":{"status_registered":93,"status_undiscoverable":87,"status_unregistered":67},"nf_cpu_usage":9,"confidence":0,"nf_set_id":"nfSetId","nf_memory_usage":6,"nf_load_level_average":6,"nf_load_avg_in_aoi":2},{"nf_instance_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","snssai":{"sd":"sd","sst":37},"nf_storage_usage":3,"nf_load_levelpeak":1,"nf_status":{"status_registered":93,"status_undiscoverable":87,"status_unregistered":67},"nf_cpu_usage":9,"confidence":0,"nf_set_id":"nfSetId","nf_memory_usage":6,"nf_load_level_average":6,"nf_load_avg_in_aoi":2}]},{"nf_load_level_infos":[{"nf_instance_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","snssai":{"sd":"sd","sst":37},"nf_storage_usage":3,"nf_load_levelpeak":1,"nf_status":{"status_registered":93,"status_undiscoverable":87,"status_unregistered":67},"nf_cpu_usage":9,"confidence":0,"nf_set_id":"nfSetId","nf_memory_usage":6,"nf_load_level_average":6,"nf_load_avg_in_aoi":2},{"nf_instance_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","snssai":{"sd":"sd","sst":37},"nf_storage_usage":3,"nf_load_levelpeak":1,"nf_status":{"status_registered":93,"status_undiscoverable":87,"status_unregistered":67},"nf_cpu_usage":9,"confidence":0,"nf_set_id":"nfSetId","nf_memory_usage":6,"nf_load_level_average":6,"nf_load_avg_in_aoi":2}]}],"cons_nf_info":"consNfInfo","event_subscriptions":[{"extra_report_req":{"end_ts":"2000-01-23T04:56:07.000+00:00","start_ts":"2000-01-23T04:56:07.000+00:00"},"tgt_ue":{"supis":[null,null],"gpsis":[null,null],"any_ue":1,"int_group_ids":[null,null]},"nf_load_lvl_thds":[{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414},{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414}],"nf_set_ids":[null,null],"snssaia":[{"sd":"sd","sst":37},{"sd":"sd","sst":37}],"app_ids":[null,null],"nf_types":["NRF","NRF"],"evt_req":{"partition_criteria":["TAC","TAC"],"grp_rep_time":4,"notif_flag":"ACTIVATE","muting_setting":{"max_no_of_notif":5,"duration_buffered_notif":9},"mon_dur":"2000-01-23T04:56:07.000+00:00","imm_rep":1,"max_report_nbr":0,"rep_period":7,"samp_ratio":12,"notif_flag_instruct":{"buffered_notifs":"SEND_ALL","subscription":"CLOSE"}},"cong_thresholds":[{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414},{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414}],"any_slice":1,"notification_method":"PERIODIC","event":"SLICE_LOAD_LEVEL","expt_ana_type":"MOBILITY","nf_instance_ids":[null,null]},{"extra_report_req":{"end_ts":"2000-01-23T04:56:07.000+00:00","start_ts":"2000-01-23T04:56:07.000+00:00"},"tgt_ue":{"supis":[null,null],"gpsis":[null,null],"any_ue":1,"int_group_ids":[null,null]},"nf_load_lvl_thds":[{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414},{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414}],"nf_set_ids":[null,null],"snssaia":[{"sd":"sd","sst":37},{"sd":"sd","sst":37}],"app_ids":[null,null],"nf_types":["NRF","NRF"],"evt_req":{"partition_criteria":["TAC","TAC"],"grp_rep_time":4,"notif_flag":"ACTIVATE","muting_setting":{"max_no_of_notif":5,"duration_buffered_notif":9},"mon_dur":"2000-01-23T04:56:07.000+00:00","imm_rep":1,"max_report_nbr":0,"rep_period":7,"samp_ratio":12,"notif_flag_instruct":{"buffered_notifs":"SEND_ALL","subscription":"CLOSE"}},"cong_thresholds":[{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414},{"svc_exp_level":1.2315135,"nf_storage_usage":5,"min_traffic_rate":"minTrafficRate","avg_traffic_rate":"avgTrafficRate","var_packet_delay":3.6160767,"nf_memory_usage":5,"speed":1.0246457,"avg_packet_delay":1,"var_packet_loss_rate":7.386282,"var_traffic_rate":2.302136,"cong_level":0,"nf_cpu_usage":1,"max_traffic_rate":"maxTrafficRate","max_packet_delay":1,"nf_load_level":6,"agg_traffic_rate":"aggTrafficRate","avg_packet_loss_rate":202,"max_packet_loss_rate":414}],"any_slice":1,"notification_method":"PERIODIC","event":"SLICE_LOAD_LEVEL","expt_ana_type":"MOBILITY","nf_instance_ids":[null,null]}],"fail_event_reports":["failEventReports","failEventReports"]}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/subscriptions/{subscriptionId}".format(subscriptionId='subscription_id_example'),
    #    headers=headers,
    #    json=nncof_events_subscription,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

