try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
except Exception as e:
    print("Error {}".format(e))


def basic_function_execute(**context):
    print("Basic function here")
    context["ti"].xcom_push(key='basic', value="basic_function_execute says hi")


def support_function_execute(**context):
    instance = context.get("ti").xcom_pull(key='basic')
    print("Got this from basic: {}".format(instance))


with DAG(
        dag_id="first_dag",
        schedule_interval="@daily",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2022, 1, 1),
        },
        catchup=False) as f:
    basic_function_execute = PythonOperator(
        task_id="basic_function_execute",
        python_callable=basic_function_execute,
        provide_context=True,
        op_kwargs={"name": "Aleksandar"},
    )

    support_function_execute = PythonOperator(
        task_id="support_function_execute",
        python_callable=support_function_execute,
        provide_context=True,
    )

basic_function_execute >> support_function_execute
