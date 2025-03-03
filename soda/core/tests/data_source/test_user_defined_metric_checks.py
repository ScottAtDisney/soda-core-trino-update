from helpers.common_test_tables import customers_test_table
from helpers.data_source_fixture import DataSourceFixture
from soda.execution.check_outcome import CheckOutcome


def test_user_defined_table_expression_metric_check(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    scan = data_source_fixture.create_test_scan()
    length_expr = "LEN" if data_source_fixture.data_source_name == "sqlserver" else "LENGTH"

    ones_expression = f"SUM({length_expr}(cst_size_txt) - {length_expr}(REPLACE(cst_size_txt, '1', '')))"

    scan.add_sodacl_yaml_str(
        f"""
      checks for {table_name}:
        - avg_surface between 1068 and 1069:
            avg_surface expression: AVG(cst_size * distance)
        - ones(cst_size_txt):
            name: There must be 3 occurrences of 1 in cst_size_text
            ones expression: {ones_expression}
            warn: when < 3
            fail: when < 2
    """
    )
    scan.execute()

    avg_surface_check = scan._checks[0]
    avg_surface = avg_surface_check.check_value
    assert isinstance(avg_surface, float)
    assert 1068 < avg_surface < 1069
    assert avg_surface_check.outcome == CheckOutcome.PASS

    ones_check = scan._checks[1]
    assert ones_check.check_value == 2
    assert ones_check.check_cfg.name == "There must be 3 occurrences of 1 in cst_size_text"
    assert ones_check.outcome == CheckOutcome.WARN


def test_user_defined_table_expression_metric_check_with_variables(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    scan = data_source_fixture.create_test_scan()
    scan.add_variables({"dist": "distance"})
    scan.add_sodacl_yaml_str(
        f"""
          checks for {table_name}:
            - avg_surface between 1068 and 1069:
                avg_surface expression: AVG(cst_size * ${{dist}})
        """
    )
    scan.execute()

    scan.assert_all_checks_pass()

    avg_surface = scan._checks[0].check_value
    assert isinstance(avg_surface, float)
    assert 1068 < avg_surface < 1069


def test_user_defined_data_source_query_metric_check(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    qualified_table_name = data_source_fixture.data_source.qualified_table_name(table_name)

    scan = data_source_fixture.create_test_scan()
    scan.add_sodacl_yaml_str(
        f"""
          checks:
            - avg_surface between 1068 and 1069:
                avg_surface query: |
                  SELECT AVG(cst_size * distance) as avg_surface
                  FROM {qualified_table_name}
        """
    )
    scan.execute()

    scan.assert_all_checks_pass()

    avg_surface = scan._checks[0].check_value
    assert isinstance(avg_surface, float)
    assert 1068 < avg_surface < 1069


def test_user_defined_data_source_query_metric_check_with_variable(data_source_fixture: DataSourceFixture):
    table_name = data_source_fixture.ensure_test_table(customers_test_table)

    qualified_table_name = data_source_fixture.data_source.qualified_table_name(table_name)

    scan = data_source_fixture.create_test_scan()
    scan.add_variables({"dist": "distance"})
    scan.add_sodacl_yaml_str(
        f"""
              checks:
                - avg_surface between 1068 and 1069:
                    avg_surface query: |
                      SELECT AVG(cst_size * ${{dist}}) as avg_surface
                      FROM {qualified_table_name}
            """
    )
    scan.execute()

    scan.assert_all_checks_pass()

    avg_surface = scan._checks[0].check_value
    assert isinstance(avg_surface, float)
    assert 1068 < avg_surface < 1069
