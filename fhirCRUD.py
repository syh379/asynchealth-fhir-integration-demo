# Imports the types Dict and Any for runtime type hints.
import json
from typing import Any, Dict  
# Imports the Google API Discovery Service.
from googleapiclient import discovery

project_id = 'asynchealth-fhir-integration'
location = 'us-west2'
dataset_id = 'test-fhir-dataset-1'
fhir_store_id = 'test-fhir-store-1'

def create_patient(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
) -> Dict[str, Any]:
    """Creates a new Patient resource in a FHIR store.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store that holds the Patient resource.

    Returns:
      A dict representing the created Patient resource.
    """


    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)


    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    patient_body = {
        "name": [{"use": "official", "family": "Doe", "given": ["Katherine"]}],
        "gender": "female",
        "birthDate": "1982-06-21",
        "resourceType": "Patient",
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type="Patient", body=patient_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()

    print(f"Created Patient resource with ID {response['id']}")
    return response



def update_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Updates the entire contents of a FHIR resource.

    Creates a new current version if the resource already exists, or creates
    a new resource with an initial version if no resource already exists with
    the provided ID.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#update
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the resource. The ID is assigned by the
        server.

    Returns:
      A dict representing the updated FHIR resource.
    """

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    # The following sample body works with a Patient resource and isn't guaranteed
    # to work with other types of FHIR resources. If necessary,
    # supply a new body with data that corresponds to the resource you
    # are updating.
    patient_body = {
        "resourceType": resource_type,
        "active": True,
        "id": resource_id,
        "gender": "male",
        "birthDate": "1980-05-01",
        "name": [{"use": "official", "family": "Doe", "given": ["Katherine"]}],
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .update(name=fhir_resource_path, body=patient_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()

    print(
        f"Updated {resource_type} resource with ID {resource_id}:\n"
        f" {json.dumps(response, indent=2)}"
    )

    return response



def get_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Gets the contents of a FHIR resource.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#read
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of FHIR resource.
      resource_id: The "logical id" of the resource you want to get the contents
        of. The ID is assigned by the server.

    Returns:
      A dict representing the FHIR resource.
    """
    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)


    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .read(name=fhir_resource_path)
    )
    response = request.execute()
    print(
        f"Got contents of {resource_type} resource with ID {resource_id}:\n",
        json.dumps(response, indent=2),
    )

    return response

def delete_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    resource_type: str,
    resource_id: str,
) -> dict:
    """Deletes all versions of a FHIR resource (excluding the current version).

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#Resource_purge
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store.
      resource_type: The type of the FHIR resource.
      resource_id: The "logical id" of the resource. The ID is assigned by the
        server.

    Returns:
      An empty dict.
    """
    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .delete(name=fhir_resource_path)
    )
    response = request.execute()
    print(f"Deleted {resource_type} resource with ID {resource_id}.")

    return response


patient = create_patient(project_id, location, dataset_id, fhir_store_id)
update_resource(project_id, location, dataset_id, fhir_store_id, "Patient", patient["id"])
get_resource(project_id, location, dataset_id, fhir_store_id, "Patient", patient["id"])
delete_resource(project_id, location, dataset_id, fhir_store_id, "Patient", patient["id"])