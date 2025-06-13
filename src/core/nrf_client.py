# create dict for NF information


def get_nf_info(nf_type: str) -> dict:
    """
    Get NF information based on NF type and ID.

    Args:
        nf_type (str): The type of the NF (e.g., "AMF", "SMF").
        nf_id (str): The ID of the NF.

    Returns:
        dict: A dictionary containing NF information.
    """

    nfs = {
        "AMF": {
            "instance_id": "amf-1",
            "uri": "http://localhost:8082/subscriptions",
        },
        "SMF": {
            "instance_id": "smf-1",
            "uri": "http://localhost:8083/subscriptions",
        },
    }

    return nfs.get(nf_type, {})
