import chart_reader
import yaml
from unittest.mock import Mock
import logging


def test_read():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.read("test/test-chart")
    assert result == {'name': 'test-chart', 'appVersion': '1.16.0', 'apiVersion': 'v2', 'version': '0.1.0', 'description': 'A Helm chart for Kubernetes', 'type': 'application', 'dependencies': [{'name': 'postgresql', 'condition': 'postgresql.enabled', 'version': '1.2.3', 'repository': 'https://lol.de/repo/'}, {'name': 'mysql', 'condition': 'mysql.enabled', 'version': '1.2.3', 'repository': 'https://lol.de/repo/'}], 'values': [{'name': 'replicaCount', 'description': 'how many replicas to deploy\n', 'default': 1, 'example': ''}, {'name': 'image', 'description': 'which image to deploy\n', 'default': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''}, 'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'}], 'templates': ['deployment.yaml', 'ingress.yaml', 'service.yaml', 'hpa.yaml', 'serviceaccount.yaml'], 'objects': [{'kind': 'Deployment', 'fromTemplate': 'deployment.yaml'}, {'kind': 'Ingress', 'fromTemplate': 'ingress.yaml'}, {'kind': 'Service', 'fromTemplate': 'service.yaml'}, {'kind': 'HorizontalPodAutoscaler', 'fromTemplate': 'hpa.yaml'}, {'kind': 'ServiceAccount', 'fromTemplate': 'serviceaccount.yaml'}], 'commands': [{'description': '', 'command': ''}]}


def test_generate_chart_metadata_real_file():
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    assert result == {
        'apiVersion': 'v2',
        'appVersion': '1.16.0',
        'description': 'A Helm chart for Kubernetes',
        'name': 'test-chart',
        'type': 'application',
        'version': '0.1.0'
    }


def test_generate_chart_metadata_unknown():
    mocked_content = {}
    real_yaml_load = chart_reader.yaml.safe_load
    chart_reader.yaml.safe_load = Mock(return_value=mocked_content)
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    chart_reader.yaml.safe_load = real_yaml_load
    assert result == {
        'apiVersion': 'unknown',
        'appVersion': 'unknown',
        'description': 'unknown',
        'name': 'unknown',
        'type': 'unknown',
        'version': 'unknown'
    }

def test_generate_values_doc_and_example():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-stella")
    assert result["values"] == [
        {
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': 1, 'example': ''
        },
        {
            'name': 'image',
            'description': 'which image to deploy\n',
            'default': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''},
            'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'
        }
    ]


def test_generate_values_doc_only():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-stella-only")
    assert result["values"] == [
        {
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': 1, 'example': ''
        }
    ]


def test_generate_requirements():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_requirements(doc, "test/test-chart")
    assert result["dependencies"] == [
        {
            "name": "postgresql",
            "condition": "postgresql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        },
        {
            "name": "mysql",
            "condition": "mysql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        }
    ]


def test_generate_templates():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_templates(doc, "test/test-chart")
    assert result["templates"] == [
        "deployment.yaml",
        "ingress.yaml",
        "service.yaml",
        "hpa.yaml",
        "serviceaccount.yaml"
    ]


def test_generate_objects():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [
            "deployment.yaml",
            "hpa.yaml",
            "ingress.yaml",
            "service.yaml",
            "serviceaccount.yaml"
        ],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_objects(doc, "test/test-chart")
    assert result["objects"] == [
        {
            "kind": "Deployment",
            "fromTemplate": "deployment.yaml"
        },
        {
            "kind": "HorizontalPodAutoscaler",
            "fromTemplate": "hpa.yaml"
        },
        {
            "kind": "Ingress",
            "fromTemplate": "ingress.yaml"
        },
        {
            "kind": "Service",
            "fromTemplate": "service.yaml"
        },
        {
            "kind": "ServiceAccount",
            "fromTemplate": "serviceaccount.yaml"
        }
    ]
