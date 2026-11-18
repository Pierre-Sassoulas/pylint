#!/usr/bin/env python3
"""Clean up Cloudflare Pages deployments from unwanted branches."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

PROJECT = "onvif-python"
KEEP_BRANCHES = {"main", "dev"}
API_BASE = "https://api.cloudflare.com/client/v4"
PER_PAGE = 20
DELETABLE_STATUSES = {"success", "failure", "idle"}


def api_request(token: str, url: str, method: str = "GET") -> dict:
    """Send a request to the Cloudflare API."""
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Cloudflare API returned HTTP {exc.code}: {detail}"
        ) from exc

    if not payload.get("success"):
        raise RuntimeError(f"Cloudflare API error: {payload.get('errors')}")

    return payload


def get_branch(deployment: dict) -> str | None:
    """Extract the branch name from a deployment."""
    trigger = deployment.get("deployment_trigger") or {}
    metadata = trigger.get("metadata") or {}
    source = deployment.get("source") or {}
    config = source.get("config") or {}

    return metadata.get("branch") or deployment.get("branch") or config.get("branch")


def get_status(deployment: dict) -> str:
    """Extract the normalized deployment status."""
    stage = deployment.get("latest_stage") or {}

    return (stage.get("status") or deployment.get("status") or "").lower()


def get_created_on(deployment: dict) -> datetime:
    """Parse the deployment creation timestamp."""
    value = deployment.get("created_on") or ""

    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp
    except (ValueError, TypeError):
        return datetime.min.replace(tzinfo=timezone.utc)


def list_deployments(token: str, account_id: str) -> list[dict]:
    """Retrieve every deployment using API pagination."""
    deployments = []
    page = 1

    while True:
        url = (
            f"{API_BASE}/accounts/{account_id}"
            f"/pages/projects/{PROJECT}/deployments"
            f"?page={page}&per_page={PER_PAGE}"
        )

        payload = api_request(token, url)
        batch = payload.get("result", [])

        if not batch:
            break

        deployments.extend(batch)
        print(f"Fetched page {page}: {len(batch)} deployments")

        if len(batch) < PER_PAGE:
            break

        page += 1

    return deployments


def main() -> None:
    """List eligible deployments and optionally delete them."""
    parser = argparse.ArgumentParser(
        description=f"Clean up Cloudflare Pages deployments for {PROJECT}."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete deployments; default is dry-run.",
    )
    args = parser.parse_args()

    token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    if not token or not account_id:
        sys.exit("Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID first.")

    try:
        deployments = list_deployments(token, account_id)
    except (RuntimeError, urllib.error.URLError) as exc:
        sys.exit(f"Could not list deployments: {exc}")

    if not deployments:
        print("No deployments found.")
        return

    candidates = []
    skipped_unknown = 0
    skipped_status = 0
    kept_success = {}

    # Find the newest successful deployment on each protected branch.
    for branch in KEEP_BRANCHES:
        successful = [
            deployment
            for deployment in deployments
            if get_branch(deployment) == branch and get_status(deployment) == "success"
        ]

        if successful:
            newest = max(successful, key=get_created_on)
            kept_success[branch] = newest.get("id")

    for deployment in deployments:
        branch = get_branch(deployment)
        status = get_status(deployment)
        deployment_id = deployment.get("id")

        if not branch:
            skipped_unknown += 1
            continue

        if status not in DELETABLE_STATUSES:
            skipped_status += 1
            continue

        # Preserve only the newest successful deployment on each protected branch.
        if (
            branch in KEEP_BRANCHES
            and status == "success"
            and deployment_id == kept_success.get(branch)
        ):
            continue

        candidates.append(deployment)

    print(f"\nProject: {PROJECT}")
    print(f"Total deployments: {len(deployments)}")
    print(f"Protected branches: {', '.join(sorted(KEEP_BRANCHES))}")
    print(f"Deployments eligible for deletion: {len(candidates)}")
    print(f"Skipped deployments with unknown branch: {skipped_unknown}")
    print(f"Skipped deployments with other statuses: {skipped_status}")

    if not candidates:
        print("\nNothing to delete.")
        return

    print("\nDeployments eligible for deletion:")

    for deployment in candidates:
        print(
            f"- {get_branch(deployment):<24} "
            f"{get_status(deployment):<10} "
            f"{deployment.get('created_on', '?'):<28} "
            f"{deployment.get('id', '')} "
            f"aliases={deployment.get('aliases') or []}"
        )

    if not args.delete:
        print("\nDry-run only. No deployments were deleted.")
        print("Review the list, then rerun with --delete to proceed.")
        return

    confirmation = input(
        f"\nType DELETE to delete these {len(candidates)} deployments: "
    )

    if confirmation != "DELETE":
        print("Cancelled.")
        return

    deleted = 0
    failed = 0

    for deployment in candidates:
        deployment_id = deployment.get("id")
        branch = get_branch(deployment)

        url = (
            f"{API_BASE}/accounts/{account_id}/pages/projects/"
            f"{PROJECT}/deployments/{deployment_id}?force=true"
        )

        try:
            api_request(token, url, method="DELETE")
            print(f"DELETED  {branch}: {deployment_id}")
            deleted += 1
        except (RuntimeError, urllib.error.URLError) as exc:
            print(f"FAILED   {branch}: {deployment_id}: {exc}")
            failed += 1

    print(f"\nFinished. Deleted: {deleted}; failed: {failed}")


if __name__ == "__main__":
    main()

