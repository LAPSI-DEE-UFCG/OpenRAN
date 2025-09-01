# xApp Deployment Guide on Near-RT RIC

This guide outlines the step-by-step process for onboarding, building, pushing, and installing xApps on the OSC Near-RT RIC Kubernetes cluster.

---

## 1. Onboard do xApp

Before building the container, onboard the xApp using the DMS CLI. This registers the xApp in the system:

```bash
dms_cli onboard <CONFIG_FILE_PATH> <SCHEMA_PATH>
```

* `<CONFIG_FILE_PATH>`:  Path to the xApp **config file** (`.json`).
* `<SCHEMA_PATH>`: Path to the **schema file** that validates the config file (`.json`).

---

## 2. List Available Charts

To check the charts available in DMS, run:

```bash
dms_cli get_charts_list
```

This helps confirm if the xApp has been onboarded correctly.

---

## 3. Build the xApp Docker Image

In the xApp root directory, build the Docker image:

```bash
docker build . -t 127.0.0.1:5001/<XAPP_NAME>:<XAPP_VERSION> --network host
```

* `<XAPP_NAME>`: Name of the xApp.
* `<XAPP_VERSION>`: Version of the xApp.
* `--network host`: Allows the build to use the host network, useful for internal connections.

Verify that the image was created successfully:

```bash
docker images
```

---

## 4. Push the Image to the Local Repository

After building, push the Docker image to the repository:

```bash
docker push <REPOSITORY>:<TAG>
```

* `<REPOSITORY>`: Repository address  (e.g., `127.0.0.1:5001/<XAPP_NAME>`).
* `<TAG>`: xApp version (e.g.: `v1.0.0`).

---

## 5. Install the xApp on the Cluster

With the image available in the repository, install the xApp in the desired **namespace**:

```bash
dms_cli install <XAPP_NAME> <XAPP_VERSION> <NAMESPACE>
```

* `<NAMESPACE>`: Kubernetes namespace where the xApp will run.

---

## 6. Debug: Check Pods and Services

To verify that the xApp is running and ports are open, use the following commands:

```bash
kubectl -n <NAMESPACE> get pods    # Lista os pods do namespace
kubectl -n <NAMESPACE> get svc     # Lista os serviços e portas abertas
```

---

## 7. Uninstall the xApp

If needed, the xApp can be removed from the cluster with:

```bash
dms_cli uninstall <XAPP_NAME> <NAMESPACE>
```

---

## Notes

* Ensure **Docker** and **DMS CLI** are correctly configured in your environment.
*  The paths to the config file and schema must be accessible on the host where the command is executed.
* It is recommended to always check the **pod logs** in Kubernetes to confirm the xApp is running correctly.

---

## xApp Structure in Near-RT RIC

In the OSC Near-RT RIC Kubernetes cluster, each **xApp** is deployed as a pod, which may contain **one or more Docker containers** and a set of **services** responsible for exposing the pod's open ports. The information needed to build the pod and its services is defined in the **xApp descriptor**, known as the **config file** (optional).

To ensure correct syntax in the control section, a schema file may accompany the config file. Both files are **.json** and are typically located within the **init/ **directory.
