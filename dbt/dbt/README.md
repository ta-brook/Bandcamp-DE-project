## Setup

1. Copy both `docker-compose.yaml` and `Dockerfile`

    1.1 Create your `profile.yml` in directory `~/.dbt` or if not the dbt will ask a lot of question while install
    ```yml
    bandcamp: # project name
    outputs:
      dev:
        dataset: <bigquery dataset>
        fixed_retries: 1
        keyfile: /.google/credentials/google_credentials.json # google credentials path
        location: US 
        method: service-account
        priority: interactive
        project: <GCP project ID>
        threads: 4
        timeout_seconds: 300
        type: bigquery
    target: dev
    ```

    1.2 Config
    ```yml
    version: '3'
    services:
      bandcamp: # project name
        build:
          context: .
          target: dbt-bigquery
        image: dbt/bigquery
        volumes:
          - .:/usr/app # dbt persisting data
          - /.dbt/bandcamp/:/root/.dbt/ # `profile.yml` path
          - ~/.google/credentials/google_credentials.json:/.google/credentials/google_credentials.json # google credentials path
        network_mode: host
    ```
        
2. Run `docker compose build`

3. Run `docker compose run bandcamp init`

    3.1 input the `project name` and maybe some other config as well (see `profile.yml` above)

4. Run `docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" bandcamp debug`

After, step 4 you should get something like: `All checks passed!`

## Run dbt command by docker

- all dbt command by [official](https://docs.getdbt.com/reference/dbt-commands)

- Run dbt model

```bash
docker compose run \
  --workdir="//usr/app/dbt/bandcamp" \
  bandcamp\
  run
```


- to access docker compose and run dbt command normmal use:

```bash
docker compose run --entrypoint='bash' bandcamp
```

**However I still can't run `dbt docs serve` but any other command is working fine. so, I'll try to figure this out somehow**