# Development environments for cloud agents · Cursor

- BestBlogs URL: https://www.bestblogs.dev/en/article/4ba0b250
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 2404
- Original publisher URL: https://cursor.com/changelog/05-13-26

---

To take engineering tasks from start to finish, agents need a development environment similar to the setup on your laptop: cloned repositories, installed dependencies, credentials for internal toolchains, and access to build systems.

This release introduces new tools for teams to configure development environments for their agents. Cursor also can use these tools to set up and maintain environments for you. Together, this makes it easier for teams to run fleets of parallelized agents that handle tasks from end-to-end, inside development environments you fully control.

Multi-repo environments

Cloud agents and automations now support multi-repo environments, building off our work on multi-root workspaces. You can configure a single environment with all the repositories an agent needs for its work, with re-use across sessions.

Environment configuration as code

To make it easier to change, debug, and review environment definitions, we have improved Dockerfile-based configuration.

This includes support for build secrets, making it easy to securely access private package registries directly from your Dockerfiles. Build secrets are scoped to the build step and aren't passed to the running agent's environment.

We've also upgraded layer caching, so that only the updated layers of your image rebuild when you change the Dockerfile. Builds that hit the cache run 70% faster.

Improved agent-led environment setup

As Cursor configures your environment, it will ask you questions, flag missing credentials, and validate that your environment is set up properly.

Cursor will always show you the version of the environment your agent is running in. If your environment configuration fails, it will default to a base image with clear warning signs so that your cloud agents can keep running instead of immediately failing.

Environment governance and security controls

Every development environment now has its own version history that users can review and roll back. Admins can also restrict rollback permissions to admins only. An audit log captures every action team members take on environments, giving security teams full visibility into who changed what.

Egress and secrets can now be scoped at the development environment level. Secrets configured for one environment aren't accessible from any other.

Learn more about agent development environments in our announcement and docs.
