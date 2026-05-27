# WIZ: Cloud Hunting Game — Full Writeup

## About This CTF

The WIZ Cloud Hunting Game simulates a real-world AWS breach investigation. You're given access to cloud audit logs and live systems, and tasked with tracing attacker activity from initial exfiltration all the way to recovering stolen data from the attacker's own server.

The challenge spans cloud forensics, Linux investigation, and active threat hunting

---

## Level 1: Identifying the Exfiltration

**Goal:** Find the IAM role involved in the attack.

### Approach

S3 data event logs record object-level access including bytes transferred outbound. Sorting by `BytesOut` descending immediately surfaces the heaviest transfers — a reliable signal for data exfiltration.

```sql
SELECT * FROM s3_data_events
ORDER BY BytesOut DESC
```

The top result pointed to the `drinks` bucket, performed by:

```
************/S3Reader/drinks
```


---

## Level 2: Tracing the Compromised IAM User

**Goal:** Follow the trail of the S3Reader. Who used it?

### Approach

CloudTrail logs all AWS API calls including `AssumeRole` events. The `responseElements` field in an `AssumeRole` event contains the session name — here, `drinks`. Filtering on this narrows the results to the exact call that created the malicious session.

```sql
SELECT * FROM cloudtrail
WHERE responseElements LIKE '%drinks%'
```

This returns the `AssumeRole` event, revealing the originating IAM user:

---

## Level 3: EC2 Instance Abuse & Lambda Backdoor

**Goal:** Follow the attacker's footsteps and find the machine that was compromised and leveraged for lateral movement.

### Approach

EC2 instances that assume IAM roles make API calls that appear in CloudTrail with an ARN containing `i-` (the instance ID format). Filtering for these isolates non-human API activity.

```sql
SELECT * FROM cloudtrail
WHERE userIdentity_ARN LIKE 'arn:aws:sts::509843726190%i-%'
```

One event stood out immediately — a `UpdateFunctionCode` call (Lambda code update), targeting a function named `credsrotator`.

---

## Level 4: Finding the Attacker's Entry Point

**Goal:** Find the IP address of another ExfilCola workload that was used as the initial entry point into the organization.

### Approach

The hints pointed to examining system logs and tu use findmnt command. The `/var/log` directory appeared suspiciously minimal:

```bash
ls -la /var/log
# Only contained a hidden file: .gK8du9

cat /var/log/.gK8du9
# "FizzShadows were here..."
findmnt
# TARGET     SOURCE
# /var/log   overlay[/work/storage/47c23ebc-2219-4b3e-b1e5-888497874643/log]
```

The real `/var/log` was hidden beneath a read-only overlay filesystem. Unmounting it exposed the genuine logs:

```bash
umount /var/log
ls -la /var/log/
# auth.log, audit/, health.log, lastlog, etc.
```

Searching `auth.log` revealed repeated SSH connections from a single external IP:

---

## Level 5: Cron Persistence, Malware Analysis & C2 Recovery

**Goal:** Delete the secret recipe from the attacker's server.

### Step 1 — Finding the Persistence Mechanism

The hint directed us to crontab. Checking the postgres user's scheduled jobs:

```bash
cat /var/spool/cron/crontabs/postgres
# 0 0 * * * bash /var/lib/postgresql/data/pg_sched
```
Inspecting the file revealed it was base64-encoded:

```bash
cat pg_sched | base64 -d
```

Decoding it revealed a bash script that reached out to a remote C2 (command-and-control) server to download and execute a second-stage payload.

### Step 2 — Connecting to the C2 Server

The decoded script contained username password and a server address for the attacker's infrastructure. Connecting to the C2 server directly revealed a REST API and exposing the attacker's file collection:

```bash
curl -u USERNAME:PASSWORD SERVER_IP/
Available Endpoints:
------------------

1. List All Files
   GET /files
   Returns a list of all files in the system.

...

4. Delete File
   DELETE /files/{filename}
   Remove a file from the system.

curl -u USERNAME:PASSWORD SERVER_IP/files
Size       Date Modified         Name
--------------------------------------------------
  4.0KB  Nov 01  2025  Root Beer.txt
  5.0KB  Nov 01  2025  Man-in-the-Mojito.txt
  3.5KB  Nov 01  2025  ExfilCola-Top-Secret.txt
  4.5KB  Nov 01  2025  Prigat Overflow.txt
 ...
```

### Step 3 — Recovering the Data

The mission objective was to delete the stolen secret recipe before it could be further distributed:

```bash
curl -u USERNAME:PASSWORD -X DELETE http://SERVER_IP/files/ExfilCola-Top-Secret.txt

Success! You've deleted the secret recipe before it could be exposed.
```

---


*Part of my CTF learning journey. See the [main repo](../../README.md) for other writeups.*
