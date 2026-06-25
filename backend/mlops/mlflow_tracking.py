import mlflow


def log_research_run(
    query,
    report_length
):

    mlflow.set_experiment(
        "ResearchOS"
    )

    with mlflow.start_run():

        mlflow.log_param(
            "query",
            query
        )

        mlflow.log_metric(
            "report_length",
            report_length
        )