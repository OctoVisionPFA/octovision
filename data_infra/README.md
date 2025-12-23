# Data Infrastructure - Run Instructions

This folder contains Docker Compose configuration to run HDFS (NameNode + DataNode) and MongoDB for OctoVision.

Bring the stack up:

```bash
docker-compose -f data_infra/docker-compose.yml up -d
```

Check container status:

```bash
docker-compose -f data_infra/docker-compose.yml ps
```

Verify MongoDB:

```bash
# From host
mongo --host 127.0.0.1 --port 27017 --eval 'db.runCommand({ ping: 1 })'
```

Verify HDFS:

- NameNode web UI: http://localhost:9870
- Check NameNode logs:

```bash
docker logs -f octo_namenode
```

- Check DataNode logs:

```bash
docker logs -f octo_datanode
```

Notes:
- The HDFS images may take several minutes to download and initialize on first run.
- If you need multiple DataNodes, add additional `datanode` services in `docker-compose.yml`.
