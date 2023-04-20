import httpx
from argilla.client.api import ArgillaSingleton

def get_dataset_list(api_url, api_key):
    client = ArgillaSingleton.init(api_url, api_key)._client
    try:
        url = "{}/api/datasets".format(client.base_url)

        response = httpx.get(
            url=url,
            headers=client.get_headers(),
            cookies=client.get_cookies(),
            timeout=client.get_timeout(),
        )
        response.raise_for_status()
        response.json()
    except Exception:
        url = "{}/api/datasets/".format(client.base_url)

        response = httpx.get(
            url=url,
            headers=client.get_headers(),
            cookies=client.get_cookies(),
            timeout=client.get_timeout(),
        )
        response.raise_for_status()

    dataset_overview = []
    for dataset in response.json():
        metadata = dataset["metadata"].values()
        if (
            metadata
            and not isinstance(list(metadata)[0], str)
            and not isinstance(list(metadata)[0], int)
        ):
            metadata = list(metadata)[0].get(
                "labels", list(metadata)[0].get("entities")
            )
        else:
            metadata = None
        dataset_overview.append(
            {
                "name": dataset["name"],
                "task": dataset["task"],
                "owner": dataset["owner"],
                "id": dataset["id"],
                "labels": metadata,
            }
        )
        # if metadata is None:
        #     # dataset_overview[-1]["labels"] =
        #     setting = get_dataset_settings(dataset["name"], dataset["task"])
        #     if setting is not None:
        #         dataset_overview[-1]["labels"] = list(setting)
    return dataset_overview