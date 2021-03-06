# -*- coding: utf-8 -*-

# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

import datetime

import pytest

from glean_parser import parser
from glean_parser import metrics


def test_metrics_match_schema():
    """
    Make sure the supported set of metric types in the schema matches the set
    in `metrics.py`
    """
    schema, validator = parser._get_metrics_schema()

    assert (set(metrics.Metric.metric_types.keys()) ==
            set(schema['definitions']['metric']['properties']['type']['enum']))


def test_enforcement():
    """
    Test dataclasses enforcement.
    """
    with pytest.raises(TypeError):
        metrics.Boolean()

    # Python dataclasses don't actually validate any types, so we
    # delegate to jsonschema
    with pytest.raises(ValueError):
        metrics.Boolean(
            type='boolean',
            category='category',
            name='metric',
            bugs=[42],
            description=42,
            notification_emails=['nobody@nowhere.com']
        )


def test_isodate():
    """
    Test that expires_after_build_date is parsed into a datetime.
    """
    m = metrics.Boolean(
        type='boolean',
        category='category',
        name='metric',
        bugs=[42],
        expires_after_build_date='2018-06-10',
        notification_emails=['nobody@nowhere.com'],
        description='description...',
    )
    assert isinstance(m.expires_after_build_date, datetime.date)

    with pytest.raises(ValueError):
        m = metrics.Boolean(
            type='boolean',
            category='category',
            name='metric',
            bugs=[42],
            expires_after_build_date='foo',
            notification_emails=['nobody@nowhere.com'],
            description='description...',
        )
