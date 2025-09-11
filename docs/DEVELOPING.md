# Developing the OpenTDF Python SDK

## Enabling Direct Access Grants

In order to use token exchange with direct access grants, you will need to enable the `Direct Access Grants` option in your IdP (e.g. Keycloak)
client settings.

## Setting Up Your Development Environment

A convenience script is provided to help set up your development environment with an OpenTDF platform running in docker.

You can run the following command in your terminal:

```bash
.github/start_opentdf_docker.sh
```

Using this script will automatically enable direct access grants in Keycloak for you.
