import pytest

from airflow.models import DagBag

@pytest.fixture()
def dagbag(self):
    return DagBag()

def test_dag_loaded(self, dagbag):
    dag = dagbag.get_dag(dag_id="hello_world")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 1