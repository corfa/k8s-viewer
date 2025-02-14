from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE deployments (
            id SERIAL PRIMARY KEY,
            namespace VARCHAR(255) DEFAULT 'all-namespaces',
            image VARCHAR(255),
            time_response TIMESTAMP
        );

        CREATE TABLE envs (
            id SERIAL PRIMARY KEY,
            deployment_id INT REFERENCES deployments(id) ON DELETE CASCADE,
            name VARCHAR(255),
            value VARCHAR(255)
        );
    """,
    """
        DROP TABLE IF EXISTS envs;
        DROP TABLE IF EXISTS deployments;
    """)
]
